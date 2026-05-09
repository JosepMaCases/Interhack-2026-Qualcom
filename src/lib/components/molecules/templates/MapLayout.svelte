<script lang="ts">
    import { type Snippet } from "svelte";

    let {
        children,
        header, 
        description,
        legend, 
        notes,
    } = $props<{
        children: Snippet,
        header ?: Snippet,
        description ?: Snippet,
        legend ?: Snippet, 
        notes ?: Snippet,
    }>();
    
</script>

<div class="layout-container">
    {#if header}
        <header class="layout-header">
            {@render header()}
        </header>
    {/if}

    {#if description}
        <description class="layout-description">
            {@render description()}
        </description>
    {/if}

    <main class="layout-map-area">
        {@render children()}
    </main>

    {#if notes}
        <footer class="layout-footer">
            {@render notes()}
        </footer>
    {/if}
</div>

<style>
    .layout-container {
        width: 100vw;
        height: 100dvh; 
        display: flex;
        flex-direction: column;
        background-color: #ffffff; /*#f4f4f4; */
        padding: 0.6rem;
        box-sizing: border-box;
        overflow: hidden;
    }

    .layout-header {
        flex: 0 0 auto; 
        z-index: 10;
        font-family: 'Erode';
        font-size: 1.2rem;
        font-weight: 600;
        color: #414141;
    }

    .layout-description {
        font-size: 0.9rem;
        font-weight: 300;
        padding: 0.1rem;
        margin-top: 0.3rem;
        margin-bottom: 0.5rem;
        line-height: 1.2;
    }

    .layout-map-area {
        flex: 1; 
        position: relative; 
        background: #f4f4f4; 
        min-height: 0;
    }

    .layout-footer {
        flex: 0 0 auto;
        margin-top: 0.1rem;
        
        font-size: .5rem;
        color: #666;
    }

    @media (min-width: 768px) {
        .layout-container {
            max-width: 1200px;
        
        }
        .layout-header {
            font-size: 2rem;
            margin: 0;
        }
        .layout-description {
            font-size: 1.2rem;
            padding: 0.2rem;
            margin-bottom: 0.5rem;
        }
    }
</style>