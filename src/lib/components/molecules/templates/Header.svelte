<script>
  import Menu from '$lib/components/atoms/items/Menu.svelte';
  import { onMount } from 'svelte';

  let isScrolled = $state(false);
  let menuOpen = $state(false);
  let { isOpen = $bindable() } = $props()

  onMount(() => {
    const handleScroll = () => isScrolled = window.scrollY > 50;
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  });
</script>


<header class:sticky={isScrolled}>
  <div class="actions">
    <button class="icon-btn duck-btn" aria-label="Duck">
      <img src="/icons/duck.svg" alt="Duck Logo" />
    </button>

    <button class="icon-btn multi-btn">
      <img src="/icons/map-relief.svg" alt="Map" class="icon-map" />
      <div class="sub-icon">
        <img src="/icons/camera.svg" alt="Camera" />
      </div>
    </button>
  </div>

  <Menu isOpen={menuOpen} />
</header>

<style>
  header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem clamp(1rem, 5%, 5rem);
    z-index: 100;
    transition: var(--transition-smooth);
  }

  @media (min-width: 1800px) {
    header {
      padding: 1.5rem 10%;
    }
  }

  header.sticky {
    padding: 1rem 2rem;
  }

  .actions { display: flex; gap: 1rem; align-items: center; }

  .icon-btn {
    background: #eee;
    border: none;
    border-radius: 50%;
    width: 45px;
    height: 45px;
    cursor: pointer;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .multi-btn { width: 60px; border-radius: 30px; }
  
  .sub-icon {
    position: absolute;
    bottom: -5px;
    right: -5px;
    background: #ffee00;
    border-radius: 50%;
    width: 20px;
    height: 20px;
    padding: 3px;
  }

  img { width: 100%; height: auto; }
</style>