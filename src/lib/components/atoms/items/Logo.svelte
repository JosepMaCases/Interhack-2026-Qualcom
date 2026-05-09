<script>
  let { isScrolled = false, menuOpen = false } = $props();
</script>

<div class="logo" class:scrolled={isScrolled} class:inverted={menuOpen}>
  <a href="/">
    <span class="logo-wrapper">
      <span class="letter-s">P</span>
      <span class="rest-of-text">atitoCool</span>
    </span>
  </a>
</div>

<style>
  .logo {
    font-weight: 800;
    font-size: 1.5rem;
    z-index: 1001;
    transition: font-size 0.4s ease;
  }

  .logo-wrapper {
    display: inline-flex;
    position: relative;
    overflow: hidden; 
    padding-bottom: 4px;
  }

  /* La S y su subrayado */
  .letter-s {
    position: relative;
    display: inline-block;
  }

  .letter-s::after {
    content: "";
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 100%;
    height: 3px;
    background-color: currentColor;
    transform: scaleX(0);
    transform-origin: left;
    transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  }

  .rest-of-text {
    display: inline-block;
    max-width: 150px;
    opacity: 1;
    transition: max-width 0.4s, opacity 0.3s;
    white-space: nowrap;
  }

  .scrolled {
    font-size: 1.2rem;
  }
  .scrolled .rest-of-text {
    max-width: 0;
    opacity: 0;
    margin-right: 0;
  }
  .scrolled .letter-s::after {
    transform: scaleX(1);
  }
  .logo a {
    text-decoration: none;
    color: inherit;
  }

  .inverted a {
    color: var(--bg-color, #fff);
  }

  @media (max-width: 768px) {
    .logo {
      font-size: 1.3rem; 
    }
    .scrolled {
      font-size: 1.1rem;
    }
  }
</style>