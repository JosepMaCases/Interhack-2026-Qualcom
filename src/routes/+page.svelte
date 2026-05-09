<script lang="ts">
  import Main from "$lib/components/molecules/templates/Main.svelte";


</script>

<main class="content">
        <Main/>
</main>

<style>
    .content {
        display: flex;
        flex-direction: column;
        max-width: 1200px;
        margin: auto; 
        padding: calc(2.5rem + 2vw);
        text-align: left;
        gap: 50px;
    }
</style>