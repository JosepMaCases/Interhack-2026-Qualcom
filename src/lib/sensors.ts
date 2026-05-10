export const ARDUINO_IP = '10.103.55.238:7000';

export type Zone = 'OK' | 'FAR' | 'WARNING' | 'DANGER' | 'CRITICAL' | 'STOPPED' | 'NO_OBJECT' | string;

export type SensorData = {
  distance_mm: number | null;
  temperature_c: number | null;
  humidity_percent: number | null;
  movement?: {
    x?: number | null;
    y?: number | null;
    z?: number | null;
  };
  status?: {
    moving?: boolean;
    zone?: Zone;
    zone_code?: number;
  };
  object_detection?: {
    detected?: boolean;
    count?: number;
    labels?: string[];
    detections?: unknown[];
    proximity?: {
      state?: number;
      ratio?: number;
      label?: string | null;
      zone?: Zone;
    };
    updated_at?: string | null;
  };
  environment?: {
    synthetic?: boolean;
    updated_at?: string | null;
    traffic_episode?: boolean;
    noise?: {
      db_a?: number | null;
      zone?: Zone;
      who_limit_db_a?: number | null;
    };
    pollution?: {
      pm25_ug_m3?: number | null;
      pm10_ug_m3?: number | null;
      no2_ug_m3?: number | null;
      zone?: Zone;
      who_limits?: {
        pm25_ug_m3?: number | null;
        pm10_ug_m3?: number | null;
        no2_ug_m3?: number | null;
      };
    };
    overall_zone?: Zone;
  };
  updated_at?: string | null;
};

export async function fetchSensors(): Promise<SensorData> {
  const response = await fetch(`http://${ARDUINO_IP}/sensors`);
  if (!response.ok) throw new Error(`HTTP ${response.status}`);

  return response.json();
}

export const zoneClass = (zone: string | undefined | null) => `zone-${(zone ?? 'unknown').toLowerCase()}`;
