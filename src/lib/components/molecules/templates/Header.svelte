<script>
  import { goto } from '$app/navigation';
  import { page } from '$app/stores';

  let isScrolled = $state(false);
  let { sidebarOpen = $bindable() } = $props();
  let currentPath = '/';

  $: currentPath = $page.url.pathname;

  const handleScroll = () => {
    isScrolled = window.scrollY > 50;
  };

  const isOnMapView = () => currentPath === '/map';
  const isOnCameraView = () => currentPath === '/camera';

  const toggleMapCamera = () => {
    if (isOnMapView()) {
      // Si estás en mapa, click va a cámara
      goto('/camera');
    } else if (isOnCameraView()) {
      // Si estás en cámara, click va a mapa
      goto('/map');
    } else {
      // Si estás en cualquier otra página (home, about, etc), click va a mapa
      goto('/map');
    }
  };

  const navigateTo = (path) => {
    goto(path);
  };

  const toggleSidebar = () => {
    sidebarOpen = !sidebarOpen;
  };

  if (typeof window !== 'undefined') {
    window.addEventListener('scroll', handleScroll);
  }
</script>

<header class:sticky={isScrolled}>
  <!-- Izquierda: Dos botones de navegación -->
  <div class="nav-section">
    <button class="nav-btn" on:click={toggleMapCamera} title={isOnMapView() ? 'Ir a Cámara' : isOnCameraView() ? 'Ir a Mapa' : 'Ir a Mapa'}>
      {#if currentPath === '/map'}
        <img src="/icons/camera.svg" alt="Cámara" />
      {:else if currentPath === '/camera'}
        <img src="/icons/map-relief.svg" alt="Mapa" />
      {:else}
        <img src="/icons/map-relief.svg" alt="Mapa" />
      {/if}
    </button>

    <button class="nav-btn" on:click={() => navigateTo('/about')} title="Sobre nosotros">
      <span class="nav-text">About</span>
    </button>
  </div>

  <!-- Centro: Logo/Nombre -->
  <div class="logo-section">
    <button class="logo-btn" on:click={() => navigateTo('/')}>
      <img src="/icons/duck.svg" alt="SafeHelmet Logo" class="duck-logo" />
      <h1>SafeHelmet</h1>
    </button>
  </div>

  <!-- Derecha: Menú -->
  <div class="menu-section">
    <button class="menu-btn" on:click={toggleSidebar} title="Menú" aria-label="Abrir menú">
      <img src="/icons/menu.svg" alt="Menú" />
    </button>
  </div>
</header>

<style>
  header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    display: grid;
    grid-template-columns: auto 1fr auto;
    align-items: center;
    padding: 1rem 2rem;
    background: rgba(255, 200, 120, 0.6);
    backdrop-filter: blur(8px);
    z-index: 100;
    transition: all 0.4s cubic-bezier(0.22, 1, 0.36, 1);
    border-bottom: none;
  }

  header.sticky {
    padding: 0.75rem 2rem;
  }

  .nav-section {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }

  .logo-section {
    display: flex;
    justify-content: center;
  }

  .menu-section {
    display: flex;
    justify-content: flex-end;
  }

  .nav-btn,
  .menu-btn,
  .logo-btn {
    background: none;
    border: none;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s cubic-bezier(0.22, 1, 0.36, 1);
    font-family: inherit;
    padding: 0.5rem;
    border-radius: 8px;
  }

  .nav-btn:hover,
  .menu-btn:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
  }

  .nav-btn {
    width: 40px;
    height: 40px;
    color: #333;
  }

  .nav-btn img {
    width: 20px;
    height: 20px;
    transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  }

  .nav-btn:hover img {
    transform: scale(1.1);
  }

  .nav-text {
    font-size: 0.9rem;
    font-weight: 500;
    color: #333;
    letter-spacing: 0.5px;
  }

  .nav-text:hover {
    color: #ff8800;
  }

  .menu-btn {
    width: 40px;
    height: 40px;
    color: #333;
  }

  .menu-btn img {
    width: 18px;
    height: 18px;
    transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  }

  .menu-btn:hover img {
    transform: scale(1.1);
  }

  .logo-btn h1 {
    margin: 0;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    color: #333;
    transition: color 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  }

  .logo-btn:hover h1 {
    color: #ff8800;
  }

  .duck-logo {
    width: 28px;
    height: 28px;
    margin-right: 0.5rem;
    transition: transform 0.3s cubic-bezier(0.22, 1, 0.36, 1);
  }

  .logo-btn:hover .duck-logo {
    transform: scale(1.15) rotate(5deg);
  }

  @media (max-width: 768px) {
    header {
      grid-template-columns: 1fr auto;
      padding: 1rem;
    }

    .nav-section {
      display: none;
    }

    .logo-section {
      position: absolute;
      left: 50%;
      transform: translateX(-50%);
    }

    .menu-section {
      margin-left: auto;
    }

    .duck-logo {
      width: 24px;
      height: 24px;
    }

    .logo-btn h1 {
      font-size: 1.3rem;
    }
  }

  @media (max-width: 480px) {
    .logo-btn h1 {
      font-size: 1.2rem;
    }

    .duck-logo {
      width: 20px;
      height: 20px;
      margin-right: 0.3rem;
    }
  }
</style>