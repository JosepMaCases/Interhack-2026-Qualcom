<script>
  import { goto } from '$app/navigation';
  import { fade, slide } from 'svelte/transition';

  let { isOpen = $bindable() } = $props();
  const handleClose = () => {
    isOpen = false;
  };

</script>

{#if isOpen}
  <div class="overlay" transition:fade={{ duration: 200 }} on:click={handleClose}></div>

  <aside class="sidebar" transition:slide={{ duration: 300, axis: 'x' }}>
    <div class="sidebar-header">
      <button class="close-btn" on:click={handleClose} aria-label="Cerrar menú">
        ✕
      </button>
    </div>
    <div class="sidebar-footer">
      <p>SafeHelmet © 2026</p>
    </div>
  </aside>
{/if}

<style>
  .overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 199;
    filter:blur(8px);
  }

  .sidebar {
    position: fixed;
    top: 0;
    right: 0;
    width: 25%;
    height: 100vh;
    z-index: 200;
    display: flex;
    flex-direction: column;
    box-shadow: -2px 0 15px rgba(0, 0, 0, 0.2);
    padding-top: 70px;
  }

  .sidebar-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.5rem;
  }

  .close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #999;
    transition: color 0.3s ease;
  }

  .close-btn:hover {
    color: #333;
  }

  .sidebar-footer {
    padding: 1.5rem;
    text-align: center;
    color: #999;
    font-size: 0.85rem;
  }

  @media (max-width: 768px) {
    .sidebar {
      width: 60%;
    }
  }

  @media (max-width: 480px) {
    .sidebar {
      width: 80%;
    }
  }
</style>
