<script lang="ts">


    let props = {
        src: string,
        alt: string,
        height: Number,
        pre_h: Number, 
        credits: string

    }
    
</script>

Intentar que los componentes no tengan más de 100 lineas, muy importante. Trabajar mucho en las animaciones,
gsap para svelte? 
different options, big and medium

<div class="img-container">
    <img 
        {src} 
        {alt} 
        {width}
        {height}/>
    <div class="credits">
        <p class="credit">{credits}</p>
        <div class="filete"></div>
    </div>

</div>

<style>

</style>