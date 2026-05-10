from base64 import b64decode
from datetime import datetime, UTC
from io import BytesIO
import random
import time

from PIL import Image, ImageDraw
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse

from arduino.app_utils import *
from arduino.app_bricks.web_ui import WebUI
from arduino.app_bricks.video_objectdetection import VideoObjectDetection

logger = Logger("helmet-api")

ui = WebUI(addr="0.0.0.0", port=7000, cors_origins="")
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
    "environment": {
        "synthetic": True,
        "updated_at": None,
        "noise": {
            "db_a": 0.0,
            "zone": "OK",
            "who_limit_db_a": 53,
        },
        "pollution": {
            "pm25_ug_m3": 0.0,
            "pm10_ug_m3": 0.0,
            "no2_ug_m3": 0.0,
            "zone": "OK",
            "who_limits": {
                "pm25_ug_m3": 15,
                "pm10_ug_m3": 45,
                "no2_ug_m3": 25,
            },
        },
        "overall_zone": "OK",
    },
    "updated_at": None,
}
last_detection_seen_ts = 0
latest_detections = []
last_environment_update_ts = 0
traffic_episode_until_ts = 0
environment_state = {
    "noise_db_a": 56.0,
    "pm25_ug_m3": 10.0,
    "pm10_ug_m3": 24.0,
    "no2_ug_m3": 16.0,
}
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
API_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "*",
    "Access-Control-Allow-Private-Network": "true",
    "Cache-Control": "no-store",
}
ENVIRONMENT_INTERVAL_SEC = 2.0
WHO_LIMITS = {
    "noise_db_a": 53,
    "pm25_ug_m3": 15,
    "pm10_ug_m3": 45,
    "no2_ug_m3": 25,
}
ZONE_RANK = {
    "OK": 0,
    "WARNING": 1,
    "DANGER": 2,
    "CRITICAL": 3,
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


def clamp(value: float, min_value: float, max_value: float):
    return max(min_value, min(max_value, value))


def move_towards(current: float, target: float, max_step: float):
    delta = target - current
    if abs(delta) <= max_step:
        return target

    return current + max_step if delta > 0 else current - max_step


def zone_from_ratio(value: float, limit: float, critical_override=False):
    if critical_override or value >= limit * 2:
        return "CRITICAL"

    if value >= limit * 1.5:
        return "DANGER"

    if value > limit:
        return "WARNING"

    return "OK"


def worst_zone(*zones):
    return max(zones, key=lambda zone: ZONE_RANK.get(zone, 0))


def maybe_start_traffic_episode(now: float):
    global traffic_episode_until_ts

    if now < traffic_episode_until_ts:
        return

    if random.random() < 0.18:
        traffic_episode_until_ts = now + random.uniform(10, 22)


def update_environment():
    global last_environment_update_ts

    now = time.time()
    if now - last_environment_update_ts < ENVIRONMENT_INTERVAL_SEC:
        return

    last_environment_update_ts = now
    maybe_start_traffic_episode(now)
    traffic_active = now < traffic_episode_until_ts

    if traffic_active:
        targets = {
            "noise_db_a": random.uniform(68, 85),
            "pm25_ug_m3": random.uniform(20, 45),
            "pm10_ug_m3": random.uniform(50, 120),
            "no2_ug_m3": random.uniform(35, 75),
        }
    else:
        targets = {
            "noise_db_a": random.uniform(48, 65),
            "pm25_ug_m3": random.uniform(5, 18),
            "pm10_ug_m3": random.uniform(12, 45),
            "no2_ug_m3": random.uniform(8, 30),
        }

    environment_state["noise_db_a"] = clamp(
        move_towards(environment_state["noise_db_a"], targets["noise_db_a"], 4.5)
        + random.uniform(-1.2, 1.2),
        42,
        88,
    )
    environment_state["pm25_ug_m3"] = clamp(
        move_towards(environment_state["pm25_ug_m3"], targets["pm25_ug_m3"], 3.0)
        + random.uniform(-0.6, 0.6),
        2,
        55,
    )
    environment_state["pm10_ug_m3"] = clamp(
        move_towards(environment_state["pm10_ug_m3"], targets["pm10_ug_m3"], 8.0)
        + random.uniform(-1.5, 1.5),
        5,
        130,
    )
    environment_state["no2_ug_m3"] = clamp(
        move_towards(environment_state["no2_ug_m3"], targets["no2_ug_m3"], 5.0)
        + random.uniform(-1.0, 1.0),
        3,
        85,
    )

    noise = round(environment_state["noise_db_a"], 1)
    pm25 = round(environment_state["pm25_ug_m3"], 1)
    pm10 = round(environment_state["pm10_ug_m3"], 1)
    no2 = round(environment_state["no2_ug_m3"], 1)

    noise_zone = zone_from_ratio(
        noise,
        WHO_LIMITS["noise_db_a"],
        critical_override=noise >= 75,
    )
    pollution_zone = worst_zone(
        zone_from_ratio(pm25, WHO_LIMITS["pm25_ug_m3"]),
        zone_from_ratio(pm10, WHO_LIMITS["pm10_ug_m3"]),
        zone_from_ratio(no2, WHO_LIMITS["no2_ug_m3"]),
    )
    overall_zone = worst_zone(noise_zone, pollution_zone)

    latest_sensors["environment"] = {
        "synthetic": True,
        "updated_at": now_iso(),
        "traffic_episode": traffic_active,
        "noise": {
            "db_a": noise,
            "zone": noise_zone,
            "who_limit_db_a": WHO_LIMITS["noise_db_a"],
        },
        "pollution": {
            "pm25_ug_m3": pm25,
            "pm10_ug_m3": pm10,
            "no2_ug_m3": no2,
            "zone": pollution_zone,
            "who_limits": {
                "pm25_ug_m3": WHO_LIMITS["pm25_ug_m3"],
                "pm10_ug_m3": WHO_LIMITS["pm10_ug_m3"],
                "no2_ug_m3": WHO_LIMITS["no2_ug_m3"],
            },
        },
        "overall_zone": overall_zone,
    }


def get_camera():
    return StreamingResponse(
        camera_stream(),
        media_type="multipart/x-mixed-replace; boundary=frame",
        headers=API_HEADERS,
    )


def get_sensors():
    global latest_detections

    update_environment()

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

    return JSONResponse(content=latest_sensors, headers=API_HEADERS)


def api_options():
    return JSONResponse(content={}, headers=API_HEADERS)


try:
    Bridge.provide("record_distance", record_distance)
    Bridge.provide("record_thermo", record_thermo)
    Bridge.provide("record_movement", record_movement)
    Bridge.provide("record_status", record_status)

except RuntimeError:
    logger.debug("Bridge handlers already registered")

detection_stream.on_detect_all(record_detections)

ui.expose_api("GET", "/cam", get_camera)
ui.expose_api("OPTIONS", "/cam", api_options)
ui.expose_api("GET", "/sensors", get_sensors)
ui.expose_api("OPTIONS", "/sensors", api_options)
ui.expose_api("GET", "/api/cam", get_camera)
ui.expose_api("OPTIONS", "/api/cam", api_options)
ui.expose_api("GET", "/api/sensors", get_sensors)
ui.expose_api("OPTIONS", "/api/sensors", api_options)

App.run()
