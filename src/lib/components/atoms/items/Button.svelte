<script lang="ts">
    let {src} = $props();
</script>

<button class="btn" aria-label=btn">
    <img height="50px" width="50px" {src}/>
</button>

<style>
    .btn {
        position: relative;
        padding: 0.5rem;
        height: auto;
        width: auto;
    }
</style>