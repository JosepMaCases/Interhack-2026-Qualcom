<script lang="ts">
  import { goto } from '$app/navigation';

  let isScrolled = $state(false);
  let { sidebarOpen = $bindable() } = $props();
  let currentPath = '/';

  const handleScroll = () => {
    isScrolled = window.scrollY > 50;
  };

  const isOnMapView = () => currentPath === '/map';

  const toggleMapCamera = () => {
    if (isOnMapView()) {
      // Si estás en mapa, click va a cámara
      goto('/camera');
    } else {
      // Si estás en cámara, click va a mapa
      goto('/map');
    } 
  };

  function navigateTo(path: string) {
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
  <div class="nav-section">
    <button class="brand-btn" onclick={() => navigateTo('/about')} title="Sobre nosotros">
      <img src="/icons/logo.png" alt="Logo SafeHelmet" aria-label="duck-logo" />SafeHelmet
    </button>
    <button class="nav-btn" onclick={() => navigateTo('/map')} title="Ir a mapa">
      <img src="/icons/map-relief.svg" alt="Mapa" />
    </button>
    <button class="nav-btn" onclick={() => navigateTo('/camera')} title="Ir a Cámara">
      <img src="/icons/camera.svg" alt="Cámara" />
    </button>
    <button class="nav-btn" onclick={() => navigateTo('/stats')} title="Ir a estadisticas">
      <img src="/icons/stats.svg" alt="Estadisticas" />
    </button>
  </div>

  <div class="menu-section">
    <button class="menu-btn" onclick={toggleSidebar} title="Menú" aria-label="Abrir menú">
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
    z-index: 100;
    transition: all 0.4s cubic-bezier(0.22, 1, 0.36, 1);
    margin: 0.9rem 1.5rem 0;
    border-radius: 8px;
    background: var(--bg-color);
    backdrop-filter: blur(16px);
    box-shadow: 0 12px 36px rgba(39, 39, 39, 0.06);
  }

  header.sticky {
    padding: 0.75rem 2rem;
    background: var(--bg-color);
  }

  .nav-section {
    display: flex;
    align-items: center;
    gap: 2rem;
  }

  .menu-section {
    display: flex;
    justify-content: flex-end;
  }

  .brand-btn,
  .nav-btn,
  .menu-btn {
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
  .brand-btn:hover,
  .menu-btn:hover {
    background: rgba(39, 39, 39, 0.08);
    transform: translateY(-2px);
  }

  .brand-btn {
    width: auto;
    height: 40px;
    padding: 0.5rem 0.35rem;
    color: #3b405b;
    font-size: 1.12rem;
    font-weight: 800;
    letter-spacing: 0.01em;
    text-shadow: 0 1px 8px rgba(255, 255, 255, 0.22);
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

  img {
    height: 40px;
    width: 70px;
    object-fit: cover; 
  }
  @media (max-width: 768px) {
    header {
      grid-template-columns: 1fr auto;
      padding: 1rem;
    }

    .nav-section {
      display: none;
    }
    .menu-section {
      margin-left: auto;
    }
  }

</style>
