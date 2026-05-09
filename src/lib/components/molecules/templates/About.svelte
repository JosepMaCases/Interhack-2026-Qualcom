<script>

</script>

<section class="about-container">
  <section class="section">
    <h2>¿Quienes somos?</h2>
    <p>Somos una compañía comprometida con la seguridad vial, nuestro objetivo 
      es ayudar a mejorar cómo conducimos, desde bicicletas a patinetes. 
    </p>
  </section>
  <section class="section">
    <h2>¿Qué hacemos?</h2>
    <p></p>
  </section>
  <section class="section">
    <h2>Compra</h2>
    <button class="">Compra</button>
    <p>Somos una compañía comprometida con la seguridad vial, nuestro objetivo 
      es ayudar a mejorar cómo conducimos, desde bicicletas a patinetes. 
    </p>
  </section>
</section>

<style>
  .about-container {
    flex-direction: column;
    width: 100%;
    margin: 7rem 2rem;
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 2rem;

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


</style>