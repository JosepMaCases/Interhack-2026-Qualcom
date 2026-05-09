<script>
  import { fade } from 'svelte/transition';

  let {sections = [ 
    {
        title:"Ours",
        description: ""
     }
  ]} = $props()
</script>

<section class="about-container" transition:fade={{ duration: 300 }}>
  <div class="content">
    <article>
      <h2>Who We Are</h2>
      <p>Innovadores en seguridad vial...</p>
    </article>

    <article>
      <h2>Why?</h2>
      <p>Reducimos el tiempo de respuesta en accidentes en un 40%.</p>
    </article>

    <div class="model-3d" >
      <p class="placeholder">Cargando modelo 3D del Casco...</p>
    </div>

    <div class="buy-section">
      <button class="buy-now">Buy Now</button>
    </div>
  </div>
</section>

<style>
  .about-container { padding: 4rem 2rem; max-width: 1200px; margin: auto; }
  .model-3d { 
    height: 400px; 
    background: #1a1a1a; 
    border-radius: 15px; 
    margin: 2rem 0;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  .buy-now {
    background: #ff3e00;
    color: white;
    padding: 1rem 3rem;
    border: none;
    font-weight: bold;
    border-radius: 5px;
    cursor: pointer;
  }
  .intro-page {
        height: 100svh;
        width: 100%;
        margin: auto;
    }

    h1 {
        font-size: clamp(3rem, 8vw, 6rem); 
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: calc(2px + 0.5vw);
    }
    .subtitle {
        font-size: clamp(1.5rem, 8vw, 1.5rem); 
        font-size: 1.5rem;
        font-weight: 300;
    }
</style>