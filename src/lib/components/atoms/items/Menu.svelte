<script>
  import { fade, fly } from 'svelte/transition'; 
  import { cubicInOut } from 'svelte/easing';
  
  let {isOpen = false } = $props();
  
  const toggleMenu = () => {
    isOpen = !isOpen;
    document.body.style.overflow = isOpen ? 'hidden' : 'auto';
  };

  const menuItems = [
    { name: 'Projects', path: '/projects' },
    { name: 'Search', path: '/search' },
    { name: 'Who We Are', path: '/about' }
  ];
</script>

<button class="menu-btn" class:open={isOpen} onclick={toggleMenu} aria-label="Menu">
  <div class="line"></div>
  <div class="line"></div>
  <div class="line"></div>
</button>

{#if isOpen}
  <div class="menu-overlay" class:visible={isOpen} transition:fade={{ duration: 300 }}>
    <nav>
      <ul>
        {#each menuItems as item, i}
          <li in:fly={{ y: 20, duration: 500, delay: 200 + (i * 100), easing: cubicInOut }}>
            <a href={item.path} onclick={toggleMenu}>{item.name}</a></li>
        {/each}
      </ul>
    </nav>
  </div>
{/if}

<style>
  .menu-btn {
    background: none;
    border: none;
    cursor: pointer;
    z-index: 1001;
    display: flex;
    flex-direction: column;
    gap: 6px;
    padding: 10px;
  }

  .line {
    width: 30px;
    height: 2px;
    background-color: var(--text-color);
    transition: var(--transition-smooth);
  }

  .open .line:nth-child(1) {
    transform: translateY(8px) rotate(45deg);
    background-color: var(--bg-color)
  }
  .open .line:nth-child(2) {
    opacity: 0;
  }
  .open .line:nth-child(3) {
    transform: translateY(-8px) rotate(-45deg);
    background-color: var(--bg-color)
  }

  .menu-overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background-color:var(--text-color); 
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 1000;
    transition: var(--transition-smooth);
  }

  nav ul {
    list-style: none;
    text-align: center;
    padding: 0;
    transition: var(--transition-smooth);
  }

  nav li {
    margin: 1rem 0;
  }

  nav a {
    color: var(--bg-color);
    text-decoration: none;
    font-size: 2rem;
    font-weight: 300;
    transition: var(--transition-smooth);
  }

  nav a:hover {
    letter-spacing: 4px;
  }
</style>