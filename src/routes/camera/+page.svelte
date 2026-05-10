<script lang="ts">
  import { onDestroy, onMount } from 'svelte';
  import { ARDUINO_IP, fetchSensors, zoneClass, type SensorData } from '$lib/sensors';

  const POLL_MS = 500;
  const DETECTION_HOLD_MS = 5000;
  const NOTIFICATION_COOLDOWN_MS = 60000;
  const ALERT_ZONES = new Set(['WARNING', 'DANGER', 'CRITICAL']);

  let sensorData = $state<SensorData | null>(null);
  let connectionError = $state(false);
  let notificationPermission = $state<NotificationPermission>('default');
  let detectionStartedAt: number | null = null;
  let lastNotificationAt = 0;
  let hasNotifiedCurrentDetection = false;
  let intervalId: ReturnType<typeof setInterval>;

  const isDetected = $derived(Boolean(sensorData?.object_detection?.detected || (sensorData?.object_detection?.count ?? 0) > 0));
  const heldSeconds = $derived(detectionStartedAt ? Math.min(5, Math.floor((Date.now() - detectionStartedAt) / 1000)) : 0);
  const highNoise = $derived(isAlertZone(sensorData?.environment?.noise?.zone));
  const highPollution = $derived(isAlertZone(sensorData?.environment?.pollution?.zone));

  function isAlertZone(zone: string | null | undefined) {
    return ALERT_ZONES.has((zone ?? '').toUpperCase());
  }

  function formatValue(value: unknown, suffix = '') {
    if (typeof value !== 'number' || !Number.isFinite(value)) return '--';
    return `${Number.isInteger(value) ? value : value.toFixed(1)}${suffix}`;
  }

  function notificationBody(data: SensorData) {
    const messages = [];
    const noise = data.environment?.noise;
    const pollution = data.environment?.pollution;

    if (isAlertZone(noise?.zone)) {
      messages.push(`Soroll ${formatValue(noise?.db_a, ' dB')} (${noise?.zone}). Pot afectar la salut si es mante.`);
    }

    if (isAlertZone(pollution?.zone)) {
      messages.push(
        `Aire ${pollution?.zone}: PM2.5 ${formatValue(pollution?.pm25_ug_m3, ' ug/m3')}, NO2 ${formatValue(pollution?.no2_ug_m3, ' ug/m3')}.`
      );
    }

    return messages.join(' ');
  }

  async function enableNotifications() {
    if (!('Notification' in window)) return;
    notificationPermission = await Notification.requestPermission();
  }

  function maybeNotify(data: SensorData) {
    const now = Date.now();
    const detected = Boolean(data.object_detection?.detected || (data.object_detection?.count ?? 0) > 0);

    if (!detected) {
      detectionStartedAt = null;
      hasNotifiedCurrentDetection = false;
      return;
    }

    detectionStartedAt ??= now;

    const detectedLongEnough = now - detectionStartedAt >= DETECTION_HOLD_MS;
    const hasHealthRisk = isAlertZone(data.environment?.noise?.zone) || isAlertZone(data.environment?.pollution?.zone);
    const canNotify = notificationPermission === 'granted' && now - lastNotificationAt > NOTIFICATION_COOLDOWN_MS;

    if (!detectedLongEnough || !hasHealthRisk || !canNotify || hasNotifiedCurrentDetection) return;

    new Notification('SafeHelmet: risc ambiental', {
      body: notificationBody(data),
      tag: 'safehelmet-environment-risk'
    });

    lastNotificationAt = now;
    hasNotifiedCurrentDetection = true;
  }

  async function refreshSensors() {
    try {
      const nextData = await fetchSensors();
      sensorData = nextData;
      connectionError = false;
      maybeNotify(nextData);
    } catch (error) {
      connectionError = true;
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
  });
</script>

<svelte:head>
  <title>Camera - SafeHelmet</title>
  <meta name="description" content="Monitoreo en vivo con deteccion de colisiones activa." />
</svelte:head>

<div class="camera-demo">
  <div class="video-feed">
    <img
      class="camera-stream"
      src={`http://${ARDUINO_IP}/cam`}
      alt="Video en directe"
    />
  </div>

  <section class="camera-hud">
    <div class="hud-card">
      <span>Deteccio</span>
      <strong class:active={isDetected}>{isDetected ? `Activa ${heldSeconds}s` : 'Inactiva'}</strong>
      <small>{connectionError ? 'Sense dades de sensors' : `${sensorData?.object_detection?.count ?? 0} objectes`}</small>
    </div>

    <div class="hud-card">
      <span>Soroll</span>
      <strong class={zoneClass(sensorData?.environment?.noise?.zone)}>{formatValue(sensorData?.environment?.noise?.db_a, ' dB')}</strong>
      <small>{sensorData?.environment?.noise?.zone ?? '--'}</small>
    </div>

    <div class="hud-card">
      <span>Aire</span>
      <strong class={zoneClass(sensorData?.environment?.pollution?.zone)}>{sensorData?.environment?.pollution?.zone ?? '--'}</strong>
      <small>PM2.5 {formatValue(sensorData?.environment?.pollution?.pm25_ug_m3, ' ug/m3')}</small>
    </div>

    {#if notificationPermission !== 'granted'}
      <button class="notify-btn" onclick={enableNotifications}>
        Activar avisos
      </button>
    {:else}
      <div class:warning={highNoise || highPollution} class="notify-state">
        Avisos actius
      </div>
    {/if}
  </section>
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

  .camera-hud {
    position: absolute;
    left: 18px;
    right: 18px;
    bottom: 18px;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr)) auto;
    align-items: stretch;
    gap: 10px;
    z-index: 2;
  }

  .hud-card,
  .notify-state,
  .notify-btn {
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 8px;
    background: rgba(10, 10, 10, 0.66);
    color: #f9f9f9;
    backdrop-filter: blur(14px);
  }

  .hud-card {
    min-height: 86px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 8px;
    padding: 12px;
  }

  .hud-card span {
    color: rgba(249, 249, 249, 0.58);
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  .hud-card strong {
    font-size: 1.15rem;
    line-height: 1.1;
  }

  .hud-card strong.active {
    color: #f97316;
  }

  .hud-card small {
    color: rgba(249, 249, 249, 0.62);
  }

  .notify-btn,
  .notify-state {
    min-width: 132px;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0 14px;
    font-size: 0.82rem;
    font-weight: 800;
  }

  .notify-btn {
    cursor: pointer;
  }

  .notify-state.warning {
    color: #fbbf24;
  }

  :global(.zone-ok),
  :global(.zone-far) {
    color: #86efac !important;
  }

  :global(.zone-warning) {
    color: #fbbf24 !important;
  }

  :global(.zone-danger) {
    color: #fb923c !important;
  }

  :global(.zone-critical),
  :global(.zone-stopped) {
    color: #fca5a5 !important;
  }

  @media (max-width: 760px) {
    .camera-hud {
      grid-template-columns: 1fr 1fr;
      left: 10px;
      right: 10px;
      bottom: 10px;
    }

    .notify-btn,
    .notify-state {
      min-height: 48px;
      grid-column: span 2;
    }
  }
</style>
