from base64 import b64decode
from datetime import datetime, UTC
from io import BytesIO
import time

from PIL import Image, ImageDraw
from fastapi.responses import StreamingResponse

from arduino.app_utils import *
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.video_objectdetection import VideoObjectDetection

logger = Logger("helmet-api")

ui = WebUI(cors_origins="")
detection_stream = VideoObjectDetection(
    confidence=0.5,
    debounce_sec=0.0,
    camera_preview=True,
)

latest_sensors = {
    "distance_mm": None,
    "temperature_c": None,
    "humidity_percent": None,
    "movement": {
        "x": None,
        "y": None,
        "z": None,
    },
    "status": {
        "moving": False,
        "zone": "NO_DISTANCE",
        "zone_code": 1,
    },
    "object_detection": {
        "detected": False,
        "count": 0,
        "labels": [],
        "detections": [],
        "proximity": {
            "state": -1,
            "ratio": 0.0,
            "label": None,
            "zone": "NO_OBJECT",
        },
        "updated_at": None,
    },
    "updated_at": None,
}
last_detection_seen_ts = 0
latest_detections = []
LABEL_COLORS = [
    (0, 255, 0),
    (0, 170, 255),
    (255, 211, 0),
    (255, 80, 80),
    (191, 90, 242),
    (255, 149, 0),
    (48, 209, 88),
    (100, 210, 255),
]
PROXIMITY_TARGET_LABEL = None
PROXIMITY_MIN_CONFIDENCE = 0.7
PROXIMITY_MAX_RATIO = 0.40
PROXIMITY_THRESHOLDS = [
    PROXIMITY_MAX_RATIO / 8,
    PROXIMITY_MAX_RATIO / 4,
    PROXIMITY_MAX_RATIO / 2,
    PROXIMITY_MAX_RATIO,
]
PROXIMITY_ZONES = {
    -1: "NO_OBJECT",
    0: "FAR",
    1: "WARNING",
    2: "DANGER",
    3: "CRITICAL",
}

ZONES = {
    0: "STOPPED",
    1: "NO_DISTANCE",
    2: "FAR",
    3: "WARNING",
    4: "DANGER",
    5: "CRITICAL",
}


def now_iso():
    return datetime.now(UTC).isoformat()


def update_timestamp():
    latest_sensors["updated_at"] = now_iso()


def record_distance(distance_mm: float):
    latest_sensors["distance_mm"] = int(distance_mm)
    update_timestamp()
    print(f"Distancia: {int(distance_mm)} mm")


def record_thermo(temperature: float, humidity: float):
    latest_sensors["temperature_c"] = round(float(temperature), 1)
    latest_sensors["humidity_percent"] = round(float(humidity), 1)
    update_timestamp()
    print(f"Temperatura: {temperature:.1f} C | Humitat: {humidity:.1f} %")


def record_movement(x: float, y: float, z: float):
    latest_sensors["movement"] = {
        "x": round(float(x), 3),
        "y": round(float(y), 3),
        "z": round(float(z), 3),
    }
    update_timestamp()
    print(f"Moviment: x={x:.3f} y={y:.3f} z={z:.3f}")


def record_status(moving: int, distance_mm: int, zone_code: int):
    zone_code = int(zone_code)
    movement_state = "moving" if int(moving) == 1 else "stopped"
    zone = ZONES.get(zone_code, "UNKNOWN")

    latest_sensors["distance_mm"] = int(distance_mm)
    latest_sensors["status"] = {
        "moving": int(moving) == 1,
        "zone": zone,
        "zone_code": zone_code,
    }
    update_timestamp()
    print(f"Estat: {movement_state} | Distancia: {distance_mm} mm | Zona: {zone}")


def record_detections(detections: dict):
    global last_detection_seen_ts, latest_detections

    detected_objects = []
    labels = []

    for label, values in detections.items():
        label = str(label)
        labels.append(label)

        for value in values:
            box = value.get("bounding_box_xyxy")
            ratio = bbox_area_ratio(box, 96, 96) if box and len(box) == 4 else 0.0
            state = get_proximity_state(ratio) if ratio > 0.0 else -1

            detected_objects.append(
                {
                    "label": label,
                    "confidence": value.get("confidence"),
                    "bounding_box_xyxy": box,
                    "proximity_ratio": round(ratio, 3),
                    "proximity_state": state,
                    "proximity_zone": PROXIMITY_ZONES.get(state, "UNKNOWN"),
                }
            )

    proximity = calculate_visual_proximity(detected_objects)

    latest_sensors["object_detection"] = {
        "detected": len(detected_objects) > 0,
        "count": len(detected_objects),
        "labels": sorted(set(labels)),
        "detections": detected_objects,
        "proximity": proximity,
        "updated_at": now_iso(),
    }

    if detected_objects:
        latest_detections = detected_objects
        last_detection_seen_ts = time.time()
    else:
        latest_detections = []


def current_camera_frame():
    frame_lock = getattr(detection_stream, "_camera_preview_lock", None)
    if frame_lock is not None:
        with frame_lock:
            return getattr(detection_stream, "_last_camera_frame", None)

    return getattr(detection_stream, "_last_camera_frame", None)


def camera_stream():
    last_frame = None

    while True:
        frame = current_camera_frame()

        if frame and frame != last_frame and "," in frame:
            last_frame = frame
            _, encoded_image = frame.split(",", 1)
            image = b64decode(encoded_image)
            image = draw_detection_boxes(image)

            yield (
                b"--frame\r\n"
                b"Content-Type: image/jpeg\r\n"
                + f"Content-Length: {len(image)}\r\n\r\n".encode()
                + image
                + b"\r\n"
            )

        time.sleep(0.05)


def draw_detection_boxes(image_bytes: bytes):
    if time.time() - last_detection_seen_ts > 1.0 or not latest_detections:
        return image_bytes

    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    draw = ImageDraw.Draw(image)

    for detection in latest_detections:
        box = detection.get("bounding_box_xyxy")
        if not box or len(box) != 4:
            continue

        x1, y1, x2, y2 = [int(value) for value in box]
        detection_label = detection.get("label", "object")
        confidence = float(detection.get("confidence", 0))
        ratio = bbox_area_ratio(box, image.width, image.height)
        state = get_proximity_state(ratio)
        color = color_for_proximity(state, detection_label)
        label = f"{detection_label} {confidence:.2f} {PROXIMITY_ZONES.get(state, 'UNKNOWN')}"

        draw.rectangle((x1, y1, x2, y2), outline=color, width=4)
        text_box = draw.textbbox((x1, y1), label)
        draw.rectangle(
            (text_box[0] - 4, text_box[1] - 4, text_box[2] + 4, text_box[3] + 4),
            fill=(0, 0, 0),
        )
        draw.text((x1, y1), label, fill=color)

    output = BytesIO()
    image.save(output, format="JPEG", quality=85)
    return output.getvalue()


def color_for_label(label: str):
    label = str(label)
    index = sum(ord(character) for character in label) % len(LABEL_COLORS)
    return LABEL_COLORS[index]


def color_for_proximity(state: int, label: str):
    if state == 0:
        return (0, 255, 0)
    if state == 1:
        return (255, 211, 0)
    if state == 2:
        return (255, 149, 0)
    if state == 3:
        return (255, 59, 48)

    return color_for_label(label)


def get_proximity_state(ratio: float):
    for index, threshold in enumerate(PROXIMITY_THRESHOLDS):
        if ratio < threshold:
            return index

    return 3


def bbox_area_ratio(box, image_width: int, image_height: int):
    x1, y1, x2, y2 = [float(value) for value in box]
    width = max(0.0, x2 - x1)
    height = max(0.0, y2 - y1)
    image_area = image_width * image_height

    if image_area <= 0:
        return 0.0

    return (width * height) / image_area


def calculate_visual_proximity(detections):
    best_ratio = 0.0
    best_label = None

    for detection in detections:
        label = str(detection.get("label"))
        confidence = float(detection.get("confidence") or 0)
        box = detection.get("bounding_box_xyxy")

        if PROXIMITY_TARGET_LABEL is not None and label != PROXIMITY_TARGET_LABEL:
            continue

        if confidence < PROXIMITY_MIN_CONFIDENCE or not box or len(box) != 4:
            continue

        ratio = bbox_area_ratio(box, 96, 96)
        if ratio > best_ratio:
            best_ratio = ratio
            best_label = label

    if best_ratio == 0.0:
        return {
            "state": -1,
            "ratio": 0.0,
            "label": None,
            "zone": PROXIMITY_ZONES[-1],
        }

    state = get_proximity_state(best_ratio)
    return {
        "state": state,
        "ratio": round(best_ratio, 3),
        "label": best_label,
        "zone": PROXIMITY_ZONES[state],
    }


def get_camera():
    return StreamingResponse(
        camera_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame",
    )


def get_sensors():
    global latest_detections

    if time.time() - last_detection_seen_ts > 1.0:
        latest_sensors["object_detection"]["detected"] = False
        latest_sensors["object_detection"]["count"] = 0
        latest_sensors["object_detection"]["labels"] = []
        latest_sensors["object_detection"]["detections"] = []
        latest_sensors["object_detection"]["proximity"] = {
            "state": -1,
            "ratio": 0.0,
            "label": None,
            "zone": PROXIMITY_ZONES[-1],
        }
        latest_detections = []

    return latest_sensors


try:
    Bridge.provide("record_distance", record_distance)
    Bridge.provide("record_thermo", record_thermo)
    Bridge.provide("record_movement", record_movement)
    Bridge.provide("record_status", record_status)

except RuntimeError:
    logger.debug("Bridge handlers already registered")

detection_stream.on_detect_all(record_detections)

ui.expose_api("GET", "/cam", get_camera)
ui.expose_api("GET", "/sensors", get_sensors)

App.run()
