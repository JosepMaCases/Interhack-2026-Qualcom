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

  function navigateTo(path) { 
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
    <button class="nav-btn" onclick={() => navigateTo('/about')} title="Sobre nosotros">
      SafeHelmet
    </button>
    <button class="nav-btn" onclick={() => navigateTo('/map')} title="Ir a mapa">
      <img src="/icons/map-relief.svg" alt="Mapa" />
    </button>
    <button class="nav-btn" onclick={() => navigateTo('/camera')} title="Ir a Cámara">
      <img src="/icons/camera.svg" alt="Cámara" />
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
    border-bottom: none;
    margin: 0 1.5rem;
  }

  header.sticky {
    padding: 0.75rem 2rem;
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

  .nav-btn,
  .menu-btn, 
  .nav-text {
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
    color: var(--second-color);
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