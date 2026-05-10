<script lang="ts">
  import { onMount, onDestroy } from 'svelte';

  const ARDUINO_IP = "10.103.55.238:7000";
  
  // Estat reactiu (Svelte 5) per desar i mostrar la informació dels sensors
  let sensorData = $state<any>(null);
  let intervalId: ReturnType<typeof setInterval>;

  onMount(() => {
    const fetchSensors = async () => {
      try {
        const response = await fetch(`http://${ARDUINO_IP}/sensors`);
        if (response.ok) {
          sensorData = await response.json();
        }
      } catch (error) {
        console.error("Error de connexió amb els sensors:", error);
      }
    };
  

    // Fem una primera crida immediata en carregar el component
    fetchSensors();

    // Configurem el polling: truca a l'API cada 500 mil·lisegons (mig segon)
    intervalId = setInterval(fetchSensors, 500);
    console.log(sensorData)
  });

  onDestroy(() => {
    // És vital netejar l'interval si l'usuari canvia de pàgina, 
    // sinó el navegador seguirà fent fetch en segon pla per sempre.
    if (intervalId) clearInterval(intervalId);
  });
</script>

<svelte:head>
  <title>Cámara - SafeHelmet</title>
  <meta name="description" content="Monitoreo en vivo con detección de colisiones activa." />
</svelte:head>

<div class="camera-demo">
  <div class="video-feed">
    
    <img 
      class="camera-stream" 
      src="http://{ARDUINO_IP}/cam" 
      alt="Vídeo en directe" 
    />

    <div class="sensor-overlay">
      {#if sensorData}
        <pre>{console.log(JSON.stringify(sensorData, null, 2))}</pre>
      {/if}
    </div>

  </div>
</div>

<style>
  .camera-demo {
    position: relative;
    width: 100%;
    height: 100svh;
    background: #ffffff;
    overflow: hidden;
  }

  .video-feed {
    width: 100%;
    height: 100%;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
    background-size: 100% 2px, 3px 100%;
  }

  .scanner-line {
    width: 100%;
    height: px;
    background: rgba(0, 255, 0, 0.5);
    position: absolute;
    animation: scan 3s infinite linear;
  }
  .camera-stream {
    width: 100%;
    height: 100%;
  }

  @keyframes scan {
    from { top: 0; }
    to { top: 100%; }
  }
</style>
