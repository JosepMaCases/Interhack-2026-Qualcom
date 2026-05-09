<script>
  import { goto } from '$app/navigation';
  import { fade, slide } from 'svelte/transition';

  let { isOpen = $bindable() } = $props();

  const menuItems = [
    { label: 'Settings', icon: '⚙️', path: '/menu' },
    { label: 'Documentation', icon: '📖', path: '/menu' },
    { label: 'Support', icon: '💬', path: '/menu' },
    { label: 'Contact', icon: '📧', path: '/menu' },
  ];

  const handleClose = () => {
    isOpen = false;
  };

  const handleMenuClick = (item) => {
    goto(item.path);
    handleClose();
  };
</script>

{#if isOpen}
  <div class="overlay" transition:fade={{ duration: 200 }} on:click={handleClose}></div>

  <aside class="sidebar" transition:slide={{ duration: 300, axis: 'x' }}>
    <div class="sidebar-header">
      <h2>Menu</h2>
      <button class="close-btn" on:click={handleClose} aria-label="Cerrar menú">
        ✕
      </button>
    </div>

    <nav class="sidebar-nav">
      {#each menuItems as item (item.label)}
        <button
          class="menu-item"
          on:click={() => handleMenuClick(item)}
        >
          <span class="icon">{item.icon}</span>
          <span class="label">{item.label}</span>
        </button>
      {/each}
    </nav>

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
  }

  .sidebar {
    position: fixed;
    top: 0;
    right: 0;
    width: 25%;
    height: 100vh;
    background: white;
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
    border-bottom: 1px solid #f0f0f0;
  }

  .sidebar-header h2 {
    margin: 0;
    font-size: 1.3rem;
    font-weight: 600;
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

  .sidebar-nav {
    display: flex;
    flex-direction: column;
    flex: 1;
    padding: 1rem 0;
    list-style: none;
  }

  .menu-item {
    background: none;
    border: none;
    padding: 1rem 1.5rem;
    text-align: left;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 1rem;
    font-size: 1rem;
    color: #333;
    transition: all 0.3s ease;
    border-left: 3px solid transparent;
  }

  .menu-item:hover {
    background: #f5f5f5;
    border-left-color: #ff3e00;
    padding-left: 2rem;
  }

  .icon {
    font-size: 1.2rem;
  }

  .label {
    font-weight: 500;
  }

  .sidebar-footer {
    padding: 1.5rem;
    border-top: 1px solid #f0f0f0;
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
