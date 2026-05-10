<script lang="ts">
  import { onDestroy, onMount } from 'svelte';
  import { fade, slide } from 'svelte/transition';
  import { fetchSensors, zoneClass, type SensorData } from '$lib/sensors';

  let { isOpen = $bindable() } = $props();
  let sensorData = $state<SensorData | null>(null);
  let connectionError = $state(false);
  let intervalId: ReturnType<typeof setInterval>;

  const handleClose = () => {
    isOpen = false;
  };

  const formatValue = (value: unknown, suffix = '') => {
    if (value === null || value === undefined) return '--';
    return `${value}${suffix}`;
  };

  onMount(() => {
    const refreshSensors = async () => {
      try {
        sensorData = await fetchSensors();
        connectionError = false;
      } catch (error) {
        connectionError = true;
      }
    };

    refreshSensors();
    intervalId = setInterval(refreshSensors, 500);
  });

  onDestroy(() => {
    if (intervalId) clearInterval(intervalId);
  });
</script>

{#if isOpen}
  <button class="overlay" transition:fade={{ duration: 200 }} onclick={handleClose} aria-label="Tancar menu"></button>

  <aside class="sidebar" transition:slide={{ duration: 300, axis: 'x' }}>
    <div class="sidebar-header">
      <div>
        <span>SafeHelmet</span>
        <h2>Sensors</h2>
      </div>

      <button class="close-btn" onclick={handleClose} aria-label="Tancar menu">
        x
      </button>
    </div>

    <div class:online={!connectionError && sensorData} class:offline={connectionError || !sensorData} class="status-pill">
      {!connectionError && sensorData ? 'ONLINE' : 'OFFLINE'}
    </div>

    {#if sensorData}
      <div class="metrics">
        <article class="metric movement-card wide">
          <div>
            <span>Moviment</span>
            <strong class:movement-active={sensorData.status?.moving}>
              {sensorData.status?.moving ? 'Movent-se' : 'Quiet'}
            </strong>
          </div>

          <div class:walking={sensorData.status?.moving} class="stick-figure" aria-hidden="true">
            <div class="head"></div>
            <div class="body"></div>
            <div class="arm left"></div>
            <div class="arm right"></div>
            <div class="leg left"></div>
            <div class="leg right"></div>
          </div>

          <small>{formatValue(sensorData.movement?.x)} / {formatValue(sensorData.movement?.y)} / {formatValue(sensorData.movement?.z)}</small>
        </article>

        <article class="metric wide">
          <span>Proximitat</span>
          <strong class={zoneClass(sensorData.status?.zone)}>{formatValue(sensorData.distance_mm, ' mm')}</strong>
          <small>Distancia darrere</small>
        </article>

        <article class="metric">
          <span>Temperatura</span>
          <strong>{formatValue(sensorData.temperature_c, ' C')}</strong>
          <small>Ambient casc</small>
        </article>

        <article class="metric">
          <span>Humitat</span>
          <strong>{formatValue(sensorData.humidity_percent, ' %')}</strong>
          <small>Ambient casc</small>
        </article>

        <article class="metric">
          <span>Soroll</span>
          <strong class={zoneClass(sensorData.environment?.noise?.zone)}>{formatValue(sensorData.environment?.noise?.db_a, ' dB')}</strong>
          <small>Llimit OMS {formatValue(sensorData.environment?.noise?.who_limit_db_a, ' dB')}</small>
        </article>

        <article class="metric">
          <span>PM2.5</span>
          <strong class={zoneClass(sensorData.environment?.pollution?.zone)}>{formatValue(sensorData.environment?.pollution?.pm25_ug_m3, ' ug/m3')}</strong>
          <small>Particules fines</small>
        </article>

        <article class="metric">
          <span>NO2</span>
          <strong>{formatValue(sensorData.environment?.pollution?.no2_ug_m3, ' ug/m3')}</strong>
          <small>PM10 {formatValue(sensorData.environment?.pollution?.pm10_ug_m3, ' ug/m3')}</small>
        </article>

        <article class="metric">
          <span>Objectes</span>
          <strong>{sensorData.object_detection?.count ?? 0}</strong>
          <small>{sensorData.object_detection?.labels?.join(', ') || 'cap deteccio'}</small>
        </article>
      </div>
    {:else}
      <div class="empty-state">
        {connectionError ? 'No es pot connectar amb Arduino' : 'Carregant sensors...'}
      </div>
    {/if}

    <div class="sidebar-footer">
      <p>SafeHelmet 2026</p>
    </div>
  </aside>
{/if}

<style>
  .overlay {
    position: fixed;
    inset: 0;
    z-index: 199;
    border: none;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(8px);
    cursor: pointer;
  }

  .sidebar {
    position: fixed;
    top: 0;
    right: 0;
    width: min(380px, 32vw);
    height: 100vh;
    z-index: 200;
    display: flex;
    flex-direction: column;
    gap: 14px;
    overflow: auto;
    padding: 86px 18px 18px;
    background: rgba(248, 248, 245, 0.94);
    border-left: 1px solid rgba(39, 39, 39, 0.08);
    box-shadow: -18px 0 60px rgba(0, 0, 0, 0.18);
  }

  .sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 16px;
    padding-bottom: 14px;
    border-bottom: 1px solid rgba(39, 39, 39, 0.1);
  }

  .sidebar-header span,
  .metric span {
    color: var(--grey-color);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  h2 {
    margin-top: 4px;
    color: var(--text-color);
    font-size: 2rem;
    line-height: 1;
  }

  .close-btn {
    width: 34px;
    height: 34px;
    border: none;
    border-radius: 8px;
    background: rgba(39, 39, 39, 0.06);
    color: var(--text-color);
    cursor: pointer;
    font-size: 1rem;
  }

  .status-pill {
    align-self: flex-start;
    border-radius: 999px;
    padding: 7px 10px;
    font-size: 0.76rem;
    font-weight: 800;
  }

  .status-pill.online {
    color: #166534;
    background: #dcfce7;
  }

  .status-pill.offline {
    color: #991b1b;
    background: #fee2e2;
  }

  .metrics {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
  }

  .metric {
    min-height: 104px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 10px;
    border-radius: 8px;
    padding: 12px;
    background: #ffffff;
    border: 1px solid rgba(39, 39, 39, 0.08);
  }

  .metric.wide {
    grid-column: span 2;
  }

  .metric strong {
    color: var(--text-color);
    font-size: 1.12rem;
    line-height: 1.1;
  }

  .movement-card {
    display: grid;
    grid-template-columns: 1fr auto;
    align-items: center;
  }

  .movement-card small {
    grid-column: 1 / -1;
  }

  .movement-active {
    color: #15803d !important;
  }

  .stick-figure {
    position: relative;
    width: 42px;
    height: 62px;
  }

  .stick-figure div {
    position: absolute;
    left: 50%;
    background: var(--text-color);
    transform-origin: top center;
  }

  .stick-figure .head {
    top: 0;
    width: 16px;
    height: 16px;
    border: 3px solid var(--text-color);
    border-radius: 50%;
    background: transparent;
    transform: translateX(-50%);
  }

  .stick-figure .body {
    top: 19px;
    width: 3px;
    height: 21px;
    transform: translateX(-50%);
  }

  .stick-figure .arm,
  .stick-figure .leg {
    width: 3px;
    height: 20px;
  }

  .stick-figure .arm {
    top: 23px;
  }

  .stick-figure .leg {
    top: 39px;
  }

  .stick-figure .arm.left {
    transform: translateX(-50%) rotate(34deg);
  }

  .stick-figure .arm.right {
    transform: translateX(-50%) rotate(-34deg);
  }

  .stick-figure .leg.left {
    transform: translateX(-50%) rotate(24deg);
  }

  .stick-figure .leg.right {
    transform: translateX(-50%) rotate(-24deg);
  }

  .stick-figure.walking .arm.left,
  .stick-figure.walking .leg.right {
    animation: swing-a 0.55s infinite alternate ease-in-out;
  }

  .stick-figure.walking .arm.right,
  .stick-figure.walking .leg.left {
    animation: swing-b 0.55s infinite alternate ease-in-out;
  }

  @keyframes swing-a {
    from { transform: translateX(-50%) rotate(42deg); }
    to { transform: translateX(-50%) rotate(-24deg); }
  }

  @keyframes swing-b {
    from { transform: translateX(-50%) rotate(-42deg); }
    to { transform: translateX(-50%) rotate(24deg); }
  }

  .metric small {
    color: var(--grey-color);
    font-size: 0.76rem;
    line-height: 1.35;
  }

  .empty-state {
    border-radius: 8px;
    padding: 14px;
    background: #ffffff;
    color: var(--grey-color);
  }

  .sidebar-footer {
    margin-top: auto;
    padding-top: 8px;
    color: #999;
    font-size: 0.78rem;
  }

  .zone-ok,
  .zone-far {
    color: #15803d !important;
  }

  .zone-warning {
    color: #a16207 !important;
  }

  .zone-danger {
    color: #c2410c !important;
  }

  .zone-critical {
    color: #b91c1c !important;
  }

  @media (max-width: 900px) {
    .sidebar {
      width: min(420px, 80vw);
    }
  }

  @media (max-width: 520px) {
    .sidebar {
      width: 88vw;
      padding: 72px 12px 12px;
    }

    .metrics {
      grid-template-columns: 1fr;
    }

    .metric.wide {
      grid-column: auto;
    }
  }
</style>
