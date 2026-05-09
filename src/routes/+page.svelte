<script lang="ts">
 
  import GltfViewer from "$lib/components/molecules/templates/GTLFContainer.svelte";
</script>

<main class="content">
    
    <section class="visor-section">
        <GltfViewer modelUrl="/models/casc.glb" />
    </section>
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

    .visor-section {
        display: flex;
        flex-direction: column;
        gap: 20px;
    }
</style>