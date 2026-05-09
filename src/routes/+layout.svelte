<script>
  import "../lib/styles/global.css";
  import Header from "$lib/components/molecules/templates/Header.svelte";
  import Sidebar from "$lib/components/molecules/templates/Sidebar.svelte";

  let { children } = $props();
  let sidebarOpen = $state(false);

  $effect(() => {
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
    display: flex;
    flex-direction: column;
  }
</style>