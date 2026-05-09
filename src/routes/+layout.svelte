<script>
  import "../lib/styles/global.css";
  import Header from "$lib/components/molecules/templates/Header.svelte";
  let { children } = $props();
</script>

<Header />

<main>
  {@render children?.()}
</main>

<style>
  main {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }
</style>