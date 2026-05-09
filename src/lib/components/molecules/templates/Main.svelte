<div class="camera-demo">
  <div class="video-overlay">
    <span class="status-badge">LIVE: COLLISION DETECTION ACTIVE</span>
  </div>
  
  <div class="video-feed">
    <div class="scanner-line"></div>
  </div>
</div>

<style>
  .camera-demo {
    position: relative;
    width: 100%;
    height: 100svh;
    background: #ffffff;
    border-radius: 20px;
    overflow: hidden;
  }

  .video-feed {
    width: 100%;
    height: 100%;
    background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
    background-size: 100% 2px, 3px 100%;
  }

  .video-overlay {
    position: absolute;
    top: 20px;
    left: 20px;
    color: #0f0;
    font-family: 'Courier New', monospace;
  }

  .scanner-line {
    width: 100%;
    height: 2px;
    background: rgba(0, 255, 0, 0.5);
    position: absolute;
    animation: scan 3s infinite linear;
  }

  @keyframes scan {
    from { top: 0; }
    to { top: 100%; }
  }
</style>