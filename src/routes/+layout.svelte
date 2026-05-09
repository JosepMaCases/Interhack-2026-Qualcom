<script>
  import "../lib/styles/global.css";
  import Header from "$lib/components/molecules/templates/Header.svelte";
  import Sidebar from "$lib/components/molecules/templates/Sidebar.svelte";
  import { page } from '$app/stores';

  let { children } = $props();
  let sidebarOpen = $state(false);

  $effect(() => {
    // Cerrar sidebar cuando cambia la ruta
    sidebarOpen = false;
  });
</script>

<Header bind:sidebarOpen />
<Sidebar bind:isOpen={sidebarOpen} />

<main>
  {@render children?.()}
</main>

<style>
  main {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    padding-top: 60px;
  }
</style>