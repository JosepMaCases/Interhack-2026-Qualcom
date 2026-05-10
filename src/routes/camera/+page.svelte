<script lang="ts">
  import { onDestroy, onMount } from 'svelte';
  import { ARDUINO_IP, fetchSensors, type SensorData } from '$lib/sensors';

  const POLL_MS = 500;
  const DETECTION_HOLD_MS = 5000;
  const POPUP_DURATION_MS = 7000;
  const ALERT_COOLDOWN_MS = 45000;
  const ALERT_ZONES = new Set(['WARNING', 'DANGER', 'CRITICAL']);

  let notificationPermission = $state<NotificationPermission>('default');
  let popupMessage = $state('');
  let popupVisible = $state(false);
  let detectionStartedAt: number | null = null;
  let lastEnvironmentAlertAt = 0;
  let hasAlertedCurrentPersonDanger = false;
  let intervalId: ReturnType<typeof setInterval>;
  let popupTimeoutId: ReturnType<typeof setTimeout>;

  function isAlertZone(zone: string | null | undefined) {
    return ALERT_ZONES.has((zone ?? '').toUpperCase());
  }

  function formatValue(value: unknown, suffix = '') {
    if (typeof value !== 'number' || !Number.isFinite(value)) return '--';
    return `${Number.isInteger(value) ? value : value.toFixed(1)}${suffix}`;
  }

  function hasPersonDetection(data: SensorData) {
    const labels = data.object_detection?.labels ?? [];
    const detections = data.object_detection?.detections ?? [];

    return (
      labels.some((label) => label.toLowerCase() === 'person') ||
      detections.some((detection) => {
        if (!detection || typeof detection !== 'object') return false;
        const values = Object.values(detection);
        return values.some((value) => typeof value === 'string' && value.toLowerCase() === 'person');
      })
    );
  }

  function personDangerMessage(data: SensorData) {
    const proximity = data.object_detection?.proximity;
    if (!hasPersonDetection(data) || proximity?.zone !== 'DANGER') return '';
    return 'Person nearby: getting close to the critical zone.';
  }

  function environmentAlertMessage(data: SensorData) {
    const noise = data.environment?.noise;
    const pollution = data.environment?.pollution;
    const messages = [];

    if (isAlertZone(noise?.zone)) {
      messages.push(`Noise is high: ${formatValue(noise?.db_a, ' dB')}. Consider moving to a quieter area.`);
    }

    if (isAlertZone(pollution?.zone)) {
      messages.push(
        `Air quality is poor: PM2.5 ${formatValue(pollution?.pm25_ug_m3, ' ug/m3')}, NO2 ${formatValue(pollution?.no2_ug_m3, ' ug/m3')}.`
      );
    }

    return messages.join(' ');
  }

  function showPopup(message: string) {
    popupMessage = message;
    popupVisible = true;

    if (popupTimeoutId) clearTimeout(popupTimeoutId);
    popupTimeoutId = setTimeout(() => {
      popupVisible = false;
    }, POPUP_DURATION_MS);
  }

  async function enableNotifications() {
    if (!('Notification' in window)) return;
    notificationPermission = await Notification.requestPermission();
  }

  function sendAlert(message: string, tag: string) {
    showPopup(message);

    if (notificationPermission === 'granted') {
      new Notification('SafeHelmet', {
        body: message,
        tag
      });
    }
  }

  function maybeAlert(data: SensorData) {
    const now = Date.now();
    const detected = Boolean(data.object_detection?.detected || (data.object_detection?.count ?? 0) > 0);
    const personMessage = personDangerMessage(data);

    if (!detected) {
      detectionStartedAt = null;
      hasAlertedCurrentPersonDanger = false;
      return;
    }

    detectionStartedAt ??= now;

    if (!personMessage) {
      hasAlertedCurrentPersonDanger = false;
    } else if (!hasAlertedCurrentPersonDanger) {
      sendAlert(personMessage, 'safehelmet-person-danger');
      hasAlertedCurrentPersonDanger = true;
    }

    const detectedLongEnough = now - detectionStartedAt >= DETECTION_HOLD_MS;
    const environmentMessage = environmentAlertMessage(data);
    const canAlertEnvironment = now - lastEnvironmentAlertAt > ALERT_COOLDOWN_MS;

    if (!detectedLongEnough || !environmentMessage || !canAlertEnvironment) return;

    sendAlert(environmentMessage, 'safehelmet-environment-risk');
    lastEnvironmentAlertAt = now;
  }

  async function refreshSensors() {
    try {
      maybeAlert(await fetchSensors());
    } catch (error) {
      // The camera view keeps running even if sensor polling is temporarily unavailable.
    }
  }

  onMount(() => {
    if ('Notification' in window) {
      notificationPermission = Notification.permission;
    }

    refreshSensors();
    intervalId = setInterval(refreshSensors, POLL_MS);
  });

  onDestroy(() => {
    if (intervalId) clearInterval(intervalId);
    if (popupTimeoutId) clearTimeout(popupTimeoutId);
  });
</script>

<svelte:head>
  <title>Camera - SafeHelmet</title>
  <meta name="description" content="Live camera feed with active collision detection." />
</svelte:head>

<div class="camera-demo">
  <div class="video-feed">
    <img
      class="camera-stream"
      src={`http://${ARDUINO_IP}/cam`}
      alt="Live video"
    />
  </div>

  {#if notificationPermission !== 'granted'}
    <button class="notify-enable" onclick={enableNotifications}>
      Enable alerts
    </button>
  {/if}

  {#if popupVisible}
    <aside class="alert-popup" role="status">
      <span>Environmental alert</span>
      <strong>{popupMessage}</strong>
      <button onclick={() => (popupVisible = false)} aria-label="Close alert">x</button>
    </aside>
  {/if}
</div>

<style>
  .camera-demo {
    position: relative;
    width: 100%;
    height: 100svh;
    background: #050505;
    overflow: hidden;
  }

  .video-feed {
    width: 100%;
    height: 100%;
    background: #050505;
  }

  .camera-stream {
    width: 100%;
    height: 100%;
    object-fit: cover;
    display: block;
  }

  .notify-enable {
    position: absolute;
    right: 18px;
    bottom: 18px;
    z-index: 2;
    border: 1px solid rgba(255, 255, 255, 0.16);
    border-radius: 8px;
    padding: 11px 14px;
    background: rgba(10, 10, 10, 0.66);
    color: #f9f9f9;
    backdrop-filter: blur(14px);
    cursor: pointer;
    font-size: 0.82rem;
    font-weight: 800;
  }

  .alert-popup {
    position: absolute;
    right: 18px;
    bottom: 18px;
    z-index: 3;
    width: min(360px, calc(100vw - 36px));
    display: grid;
    grid-template-columns: 1fr auto;
    gap: 8px 12px;
    border: 1px solid rgba(251, 191, 36, 0.38);
    border-radius: 8px;
    padding: 14px;
    background: rgba(24, 24, 24, 0.88);
    color: #f9f9f9;
    box-shadow: 0 18px 60px rgba(0, 0, 0, 0.36);
    backdrop-filter: blur(16px);
    animation: popup-in 180ms ease-out;
  }

  .alert-popup span {
    color: #fbbf24;
    font-size: 0.72rem;
    font-weight: 900;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .alert-popup strong {
    grid-column: 1 / -1;
    font-size: 0.98rem;
    line-height: 1.35;
  }

  .alert-popup button {
    grid-column: 2;
    grid-row: 1;
    width: 28px;
    height: 28px;
    border: none;
    border-radius: 8px;
    background: rgba(255, 255, 255, 0.1);
    color: #f9f9f9;
    cursor: pointer;
  }

  @keyframes popup-in {
    from {
      opacity: 0;
      transform: translateY(12px);
    }

    to {
      opacity: 1;
      transform: translateY(0);
    }
  }

  @media (max-width: 560px) {
    .notify-enable,
    .alert-popup {
      right: 10px;
      bottom: 10px;
    }
  }
</style>
