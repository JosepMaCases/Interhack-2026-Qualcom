<script lang="ts">
  const ARDUINO_IP = "10.103.55.238:7000";
</script>

<svelte:head>
  <title>Camera - SafeHelmet</title>
  <meta name="description" content="Monitoreo en vivo con deteccion de colisiones activa." />
</svelte:head>

<div class="camera-demo">
  <div class="video-feed">
    <img
      class="camera-stream"
      src="http://{ARDUINO_IP}/cam"
      alt="Video en directe"
    />
  </div>
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
</style>
