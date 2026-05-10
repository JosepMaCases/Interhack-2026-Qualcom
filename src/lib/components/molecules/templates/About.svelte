<script>
    import GltfViewer from "$lib/components/molecules/templates/GTLFContainer.svelte";
</script>

<section class="about-container">
  <section class="section">
    <h2>Qui som?</h2>
    <p>
      Som una companyia compromesa amb la seguretat vial, el nostre objectiu 
      és ajudar a millorar la vida de les persones amb més seguretat vial, des de bicicletas a patinets.
    </p>
    <button class="buy-btn">COMPRA</button>
  </section>
  <section class="section">
    <section class="visor-section">
        <GltfViewer modelUrl="/models/casc.glb" />
    </section>
  </section>
</section>

<style>
  .about-container {
    display: grid;
    grid-template-columns: minmax(400px, 1fr) 2fr;
    gap: 2rem;
    margin: 7rem 2rem;
    gap: 3rem;
  }
  h2 {
    text-transform: uppercase;
    font-size: 1.3rem;
    color: var(----text-color);
    margin: 0;
  }

  p {
    font-size: clamp(1.3rem, 6vw, 2rem);
  }

  .visor-section {
      display: flex;
      flex-direction: column;
      gap: 20px;
  }

  .buy-btn {
    color: var(--bg-color);
    font-size: 1rem;
    font-weight: 500;
    background-color: var(--second-color);
    padding: 0.35rem .5rem;
    border: none;
    border-radius: 16px;
  }

</style>