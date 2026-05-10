<script lang="ts">
  import { onDestroy, onMount } from 'svelte';
  import { fetchSensors, zoneClass, type SensorData } from '$lib/sensors';

  type Sample = { ts: number; data: SensorData };
  type SeriesPoint = { x: number; y: number };
  type Metric = {
    label: string;
    value: number | null | undefined;
    suffix: string;
    zone?: string | null;
    detail: string;
  };
  type LimitItem = {
    label: string;
    value: number | null | undefined;
    limit: number | null | undefined;
    zone?: string | null;
  };

  const MAX_POINTS = 100;
  const POLL_MS = 500;
  const CHART_WIDTH = 320;
  const CHART_HEIGHT = 150;
  const CHART_PAD = 16;

  let sensorData = $state<SensorData | null>(null);
  let connectionError = $state(false);
  let history = $state<Sample[]>([]);
  let intervalId: ReturnType<typeof setInterval>;

  const latestZone = $derived(sensorData?.environment?.overall_zone ?? sensorData?.status?.zone ?? 'UNKNOWN');

  const metrics = $derived<Metric[]>([
    {
      label: 'Distancia',
      value: sensorData?.distance_mm,
      suffix: ' mm',
      zone: sensorData?.status?.zone,
      detail: 'Proximitat posterior'
    },
    { label: 'Temperatura', value: sensorData?.temperature_c, suffix: ' C', detail: 'Ambient casc' },
    { label: 'Humitat', value: sensorData?.humidity_percent, suffix: ' %', detail: 'Ambient casc' },
    {
      label: 'Soroll',
      value: sensorData?.environment?.noise?.db_a,
      suffix: ' dB',
      zone: sensorData?.environment?.noise?.zone,
      detail: `Limit ${formatValue(sensorData?.environment?.noise?.who_limit_db_a, ' dB')}`
    },
    {
      label: 'PM2.5',
      value: sensorData?.environment?.pollution?.pm25_ug_m3,
      suffix: ' ug/m3',
      zone: sensorData?.environment?.pollution?.zone,
      detail: `Limit ${formatValue(sensorData?.environment?.pollution?.who_limits?.pm25_ug_m3, ' ug/m3')}`
    },
    {
      label: 'PM10',
      value: sensorData?.environment?.pollution?.pm10_ug_m3,
      suffix: ' ug/m3',
      zone: sensorData?.environment?.pollution?.zone,
      detail: `Limit ${formatValue(sensorData?.environment?.pollution?.who_limits?.pm10_ug_m3, ' ug/m3')}`
    },
    {
      label: 'NO2',
      value: sensorData?.environment?.pollution?.no2_ug_m3,
      suffix: ' ug/m3',
      zone: sensorData?.environment?.pollution?.zone,
      detail: `Limit ${formatValue(sensorData?.environment?.pollution?.who_limits?.no2_ug_m3, ' ug/m3')}`
    },
    {
      label: 'Objectes',
      value: sensorData?.object_detection?.count ?? 0,
      suffix: '',
      zone: sensorData?.object_detection?.proximity?.zone,
      detail: sensorData?.object_detection?.labels?.join(', ') || 'Cap deteccio'
    }
  ]);

  const limitItems = $derived<LimitItem[]>([
    {
      label: 'Soroll',
      value: sensorData?.environment?.noise?.db_a,
      limit: sensorData?.environment?.noise?.who_limit_db_a,
      zone: sensorData?.environment?.noise?.zone
    },
    {
      label: 'PM2.5',
      value: sensorData?.environment?.pollution?.pm25_ug_m3,
      limit: sensorData?.environment?.pollution?.who_limits?.pm25_ug_m3,
      zone: sensorData?.environment?.pollution?.zone
    },
    {
      label: 'PM10',
      value: sensorData?.environment?.pollution?.pm10_ug_m3,
      limit: sensorData?.environment?.pollution?.who_limits?.pm10_ug_m3,
      zone: sensorData?.environment?.pollution?.zone
    },
    {
      label: 'NO2',
      value: sensorData?.environment?.pollution?.no2_ug_m3,
      limit: sensorData?.environment?.pollution?.who_limits?.no2_ug_m3,
      zone: sensorData?.environment?.pollution?.zone
    }
  ]);

  const distanceSeries = $derived(series((sample) => sample.data.distance_mm));
  const temperatureSeries = $derived(series((sample) => sample.data.temperature_c));
  const humiditySeries = $derived(series((sample) => sample.data.humidity_percent));
  const noiseSeries = $derived(series((sample) => sample.data.environment?.noise?.db_a));
  const pm25Series = $derived(series((sample) => sample.data.environment?.pollution?.pm25_ug_m3));
  const pm10Series = $derived(series((sample) => sample.data.environment?.pollution?.pm10_ug_m3));
  const no2Series = $derived(series((sample) => sample.data.environment?.pollution?.no2_ug_m3));
  function numberOrNull(value: unknown) {
    return typeof value === 'number' && Number.isFinite(value) ? value : null;
  }

  function formatValue(value: unknown, suffix = '') {
    const numeric = numberOrNull(value);
    if (numeric === null) return '--';
    return `${Number.isInteger(numeric) ? numeric : numeric.toFixed(1)}${suffix}`;
  }

  function formatTime(value: string | null | undefined) {
    if (!value) return '--';
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return '--';
    return date.toLocaleTimeString('ca-ES', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
  }

  function series(read: (sample: Sample) => number | null | undefined): SeriesPoint[] {
    return history
      .map((sample, index) => ({ x: index, y: numberOrNull(read(sample)) }))
      .filter((point): point is SeriesPoint => point.y !== null);
  }

  function bounds(groups: SeriesPoint[][]) {
    const values = groups.flat().map((point) => point.y);
    if (!values.length) return { min: 0, max: 1 };

    let min = Math.min(...values);
    let max = Math.max(...values);
    if (min === max) {
      min -= 1;
      max += 1;
    }

    const padding = (max - min) * 0.12;
    return { min: min - padding, max: max + padding };
  }

  function linePath(points: SeriesPoint[], groups: SeriesPoint[][] = [points]) {
    if (points.length < 2) return '';

    const { min, max } = bounds(groups);
    const maxX = Math.max(1, history.length - 1);

    return points
      .map((point, index) => {
        const x = CHART_PAD + (point.x / maxX) * (CHART_WIDTH - CHART_PAD * 2);
        const y = CHART_HEIGHT - CHART_PAD - ((point.y - min) / (max - min)) * (CHART_HEIGHT - CHART_PAD * 2);
        return `${index === 0 ? 'M' : 'L'} ${x.toFixed(1)} ${y.toFixed(1)}`;
      })
      .join(' ');
  }

  function areaPath(points: SeriesPoint[], groups: SeriesPoint[][] = [points]) {
    const path = linePath(points, groups);
    if (!path || points.length < 2) return '';

    const { min, max } = bounds(groups);
    const maxX = Math.max(1, history.length - 1);
    const first = points[0];
    const last = points[points.length - 1];
    const firstX = CHART_PAD + (first.x / maxX) * (CHART_WIDTH - CHART_PAD * 2);
    const lastX = CHART_PAD + (last.x / maxX) * (CHART_WIDTH - CHART_PAD * 2);
    const baseline = CHART_HEIGHT - CHART_PAD - ((min - min) / (max - min)) * (CHART_HEIGHT - CHART_PAD * 2);

    return `${path} L ${lastX.toFixed(1)} ${baseline.toFixed(1)} L ${firstX.toFixed(1)} ${baseline.toFixed(1)} Z`;
  }

  function lastPoint(points: SeriesPoint[], groups: SeriesPoint[][] = [points]) {
    if (!points.length) return null;

    const point = points[points.length - 1];
    const { min, max } = bounds(groups);
    const maxX = Math.max(1, history.length - 1);

    return {
      x: CHART_PAD + (point.x / maxX) * (CHART_WIDTH - CHART_PAD * 2),
      y: CHART_HEIGHT - CHART_PAD - ((point.y - min) / (max - min)) * (CHART_HEIGHT - CHART_PAD * 2)
    };
  }

  function ratio(value: number | null | undefined, limit: number | null | undefined) {
    const numericValue = numberOrNull(value);
    const numericLimit = numberOrNull(limit);
    if (numericValue === null || numericLimit === null || numericLimit <= 0) return null;
    return numericValue / numericLimit;
  }

  function limitX(value: number | null | undefined, limit: number | null | undefined) {
    const currentRatio = ratio(value, limit);
    if (currentRatio === null) return 16;
    return 16 + Math.min(currentRatio, 2.5) * 100;
  }

  async function refreshSensors() {
    try {
      const nextData = await fetchSensors();
      sensorData = nextData;
      connectionError = false;
      history = [...history, { ts: Date.now(), data: nextData }].slice(-MAX_POINTS);
    } catch (error) {
      connectionError = true;
    }
  }

  onMount(() => {
    refreshSensors();
    intervalId = setInterval(refreshSensors, POLL_MS);
  });

  onDestroy(() => {
    if (intervalId) clearInterval(intervalId);
  });
</script>

<svelte:head>
  <title>Stats - SafeHelmet</title>
  <meta name="description" content="Monitoratge en temps real dels sensors SafeHelmet." />
</svelte:head>

<section class="stats-page">
  <div class="stats-shell">
    <header class="stats-header">
      <div>
        <span class="eyebrow">SafeHelmet</span>
        <h1>Estadistiques</h1>
      </div>

      <div class="status-stack">
        <span class:online={!connectionError && sensorData} class:offline={connectionError || !sensorData} class="connection">
          {!connectionError && sensorData ? 'ONLINE' : 'OFFLINE'}
        </span>
        <strong class={zoneClass(latestZone)}>{latestZone}</strong>
        <small>Actualitzat {formatTime(sensorData?.updated_at)}</small>
      </div>
    </header>

    <div class="metrics-grid">
      {#each metrics as metric}
        <article class="metric-card">
          <span>{metric.label}</span>
          <strong class={zoneClass(metric.zone)}>{formatValue(metric.value, metric.suffix)}</strong>
          <small>{metric.detail}</small>
        </article>
      {/each}
    </div>

    <div class="charts-grid">
      <article class="chart-panel wide">
        <div class="panel-header">
          <div>
            <span>Seguretat</span>
            <h2>Distancia de frenada</h2>
          </div>
          <strong class={zoneClass(sensorData?.status?.zone)}>{formatValue(sensorData?.distance_mm, ' mm')}</strong>
        </div>

        <svg viewBox="0 0 {CHART_WIDTH} {CHART_HEIGHT}" role="img" aria-label="Historic de distancia">
          <path class="grid-line" d="M 16 34 H 304 M 16 75 H 304 M 16 116 H 304" />
          <path class="area distance-area" d={areaPath(distanceSeries)} />
          <path class="series distance" d={linePath(distanceSeries)} />
          {#if lastPoint(distanceSeries)}
            {@const point = lastPoint(distanceSeries)}
            <circle class="dot distance" cx={point?.x} cy={point?.y} r="4" />
          {:else}
            <text class="empty-label" x="160" y="80">Esperant dades</text>
          {/if}
        </svg>
      </article>

      <article class="chart-panel">
        <div class="panel-header">
          <div>
            <span>Confort</span>
            <h2>Temperatura / humitat</h2>
          </div>
        </div>

        <svg viewBox="0 0 {CHART_WIDTH} {CHART_HEIGHT}" role="img" aria-label="Historic de temperatura i humitat">
          <path class="grid-line" d="M 16 34 H 304 M 16 75 H 304 M 16 116 H 304" />
          <path class="series temperature" d={linePath(temperatureSeries, [temperatureSeries, humiditySeries])} />
          <path class="series humidity" d={linePath(humiditySeries, [temperatureSeries, humiditySeries])} />
          {#if temperatureSeries.length < 2 && humiditySeries.length < 2}
            <text class="empty-label" x="160" y="80">Esperant dades</text>
          {/if}
        </svg>

        <div class="legend">
          <span><i class="temperature"></i>Temperatura</span>
          <span><i class="humidity"></i>Humitat</span>
        </div>
      </article>

      <article class="chart-panel">
        <div class="panel-header">
          <div>
            <span>Entorn</span>
            <h2>Soroll ambiental</h2>
          </div>
          <strong class={zoneClass(sensorData?.environment?.noise?.zone)}>{formatValue(sensorData?.environment?.noise?.db_a, ' dB')}</strong>
        </div>

        <svg viewBox="0 0 {CHART_WIDTH} {CHART_HEIGHT}" role="img" aria-label="Historic de soroll">
          <path class="grid-line" d="M 16 34 H 304 M 16 75 H 304 M 16 116 H 304" />
          <path class="area noise-area" d={areaPath(noiseSeries)} />
          <path class="series noise" d={linePath(noiseSeries)} />
          {#if noiseSeries.length < 2}
            <text class="empty-label" x="160" y="80">Esperant dades</text>
          {/if}
        </svg>
      </article>

      <article class="chart-panel">
        <div class="panel-header">
          <div>
            <span>Aire</span>
            <h2>Particules i NO2</h2>
          </div>
          <strong class={zoneClass(sensorData?.environment?.pollution?.zone)}>{sensorData?.environment?.pollution?.zone ?? '--'}</strong>
        </div>

        <svg viewBox="0 0 {CHART_WIDTH} {CHART_HEIGHT}" role="img" aria-label="Historic de contaminacio">
          <path class="grid-line" d="M 16 34 H 304 M 16 75 H 304 M 16 116 H 304" />
          <path class="series pm25" d={linePath(pm25Series, [pm25Series, pm10Series, no2Series])} />
          <path class="series pm10" d={linePath(pm10Series, [pm25Series, pm10Series, no2Series])} />
          <path class="series no2" d={linePath(no2Series, [pm25Series, pm10Series, no2Series])} />
          {#if pm25Series.length < 2 && pm10Series.length < 2 && no2Series.length < 2}
            <text class="empty-label" x="160" y="80">Esperant dades</text>
          {/if}
        </svg>

        <div class="legend">
          <span><i class="pm25"></i>PM2.5</span>
          <span><i class="pm10"></i>PM10</span>
          <span><i class="no2"></i>NO2</span>
        </div>
      </article>

      <article class="chart-panel limit-panel">
        <div class="panel-header">
          <div>
            <span>Llindars OMS</span>
            <h2>Comparativa actual</h2>
          </div>
        </div>

        <div class="limit-chart">
          <div class="limit-axis">
            <span>0</span>
            <span>1x</span>
            <span>2x</span>
          </div>

          <svg viewBox="0 0 286 150" role="img" aria-label="Comparativa de limits OMS">
            <path class="limit-guide" d="M 116 8 V 136 M 216 8 V 136" />
            {#each limitItems as item, index}
              {@const itemRatio = ratio(item.value, item.limit)}
              {@const y = 24 + index * 32}
              <line class="limit-row" x1="16" x2="270" y1={y} y2={y} />
              <circle class="limit-dot" cx="116" cy={y} r="5" />
              <circle class={zoneClass(item.zone)} cx={limitX(item.value, item.limit)} cy={y} r="7" />
              <text x="18" y={y - 10}>{item.label}</text>
              <text x="130" y={y + 4}>{itemRatio === null ? '--' : `${itemRatio.toFixed(1)}x`}</text>
            {/each}
          </svg>
        </div>
      </article>
    </div>
  </div>
</section>

<style>
  .stats-page {
    min-height: 100svh;
    padding: 112px 20px 28px;
    background: var(--bg-color);
  }

  .stats-shell {
    width: min(1180px, 100%);
    margin: 0 auto;
  }

  .stats-header {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 18px;
    margin-bottom: 18px;
  }

  .eyebrow,
  .metric-card span,
  .panel-header span {
    color: var(--grey-color);
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
  }

  h1 {
    margin-top: 4px;
    color: var(--second-color);
    font-size: clamp(2.2rem, 6vw, 4.6rem);
    line-height: 0.95;
  }

  h2 {
    margin-top: 4px;
    color: var(--text-color);
    font-size: 1.08rem;
    line-height: 1.15;
  }

  .status-stack {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    gap: 5px;
    color: var(--grey-color);
    font-size: 0.8rem;
  }

  .connection {
    border-radius: 999px;
    padding: 7px 10px;
    font-size: 0.74rem;
    font-weight: 900;
  }

  .connection.online {
    color: #166534;
    background: #dcfce7;
  }

  .connection.offline {
    color: #991b1b;
    background: #fee2e2;
  }

  .metrics-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: 10px;
    margin-bottom: 12px;
  }

  .metric-card,
  .chart-panel {
    border: 1px solid rgba(39, 39, 39, 0.08);
    border-radius: 8px;
    background: #fff;
    box-shadow: 0 10px 32px rgba(39, 39, 39, 0.04);
  }

  .metric-card {
    min-height: 112px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    gap: 10px;
    padding: 14px;
  }

  .metric-card strong {
    color: var(--text-color);
    font-size: 1.4rem;
    line-height: 1.05;
  }

  .metric-card small,
  .status-stack small {
    color: var(--grey-color);
    line-height: 1.35;
  }

  .charts-grid {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
  }

  .chart-panel {
    min-height: 244px;
    padding: 14px;
  }

  .chart-panel.wide {
    grid-column: span 2;
  }

  .limit-panel {
    min-height: 214px;
  }

  .panel-header {
    min-height: 44px;
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 10px;
  }

  .panel-header strong {
    color: var(--text-color);
    font-size: 1rem;
    text-align: right;
    white-space: nowrap;
  }

  svg {
    width: 100%;
    display: block;
    overflow: visible;
  }

  .grid-line,
  .limit-guide {
    fill: none;
    stroke: rgba(39, 39, 39, 0.08);
    stroke-width: 1;
  }

  .series {
    fill: none;
    stroke-width: 2.5;
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  .area {
    opacity: 0.12;
    stroke: none;
  }

  .dot {
    stroke: #fff;
    stroke-width: 2;
  }

  .series.distance,
  .series.noise {
    stroke: var(--primary-color);
  }

  .distance-area,
  .noise-area,
  .dot.distance {
    fill: var(--primary-color);
  }

  .series.temperature,
  .series.pm25 {
    stroke: var(--first-color);
  }

  .legend i.temperature,
  .legend i.pm25 {
    background: var(--first-color);
  }

  .series.humidity,
  .series.pm10 {
    stroke: var(--third-color);
  }

  .legend i.humidity,
  .legend i.pm10 {
    background: var(--third-color);
  }

  .series.no2 {
    stroke: var(--second-color);
  }

  .legend i.no2 {
    background: var(--second-color);
  }

  .legend {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-top: 10px;
    color: var(--grey-color);
    font-size: 0.78rem;
    font-weight: 700;
  }

  .legend span {
    display: inline-flex;
    align-items: center;
    gap: 6px;
  }

  .legend i {
    width: 9px;
    height: 9px;
    border-radius: 50%;
  }

  .limit-chart {
    display: grid;
    grid-template-columns: 42px 1fr;
    align-items: stretch;
    gap: 8px;
  }

  .limit-axis {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 10px 0 12px;
    color: var(--grey-color);
    font-size: 0.72rem;
    font-weight: 800;
  }

  .limit-row {
    stroke: rgba(39, 39, 39, 0.055);
    stroke-width: 10;
    stroke-linecap: round;
  }

  .limit-dot {
    fill: rgba(39, 39, 39, 0.22);
  }

  text {
    fill: #888;
    font-size: 11px;
    font-weight: 800;
  }

  .empty-label {
    fill: rgba(136, 136, 136, 0.75);
    font-size: 13px;
    text-anchor: middle;
  }

  :global(.zone-ok),
  :global(.zone-far) {
    color: #15803d !important;
    fill: #15803d;
  }

  :global(.zone-warning) {
    color: #a16207 !important;
    fill: #f59e0b;
  }

  :global(.zone-danger) {
    color: #c2410c !important;
    fill: #f97316;
  }

  :global(.zone-critical),
  :global(.zone-stopped) {
    color: #b91c1c !important;
    fill: #b91c1c;
  }

  :global(.zone-no_object),
  :global(.zone-unknown) {
    color: #888 !important;
    fill: #888;
  }

  @media (max-width: 900px) {
    .stats-page {
      padding: 94px 12px 18px;
    }

    .stats-header {
      align-items: flex-start;
      flex-direction: column;
    }

    .status-stack {
      align-items: flex-start;
    }

    .metrics-grid {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }

    .charts-grid {
      grid-template-columns: 1fr;
    }

    .chart-panel.wide {
      grid-column: auto;
    }
  }

  @media (max-width: 520px) {
    .metrics-grid {
      grid-template-columns: 1fr;
    }

    .chart-panel {
      min-height: 226px;
      padding: 12px;
    }

    .limit-chart {
      grid-template-columns: 1fr;
    }

    .limit-axis {
      flex-direction: row;
      padding: 0;
    }
  }
</style>
