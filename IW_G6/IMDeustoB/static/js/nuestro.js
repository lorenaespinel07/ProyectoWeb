document.addEventListener('DOMContentLoaded', () => {
    let paginaActual = 1;
    let paginasTotales = 2;
    const botonIzquierdo = document.querySelector('.pagination2 .ion-arrow-left-b').parentElement;
    const botonDerecho = document.querySelector('.pagination2 .ion-arrow-right-b').parentElement;
    const listaPelis = document.querySelector('.flex-wrap-movielist');
    const paginaActualSpan = document.querySelector('.pagination2 span span');
    const paginaTotalSpan = document.querySelector('.pagination2 span span:nth-child(2)');
    const buscador = document.querySelector('.top-search input');
    const resulTotal = document.querySelector('.topbar-filter p span');

    async function llamarAPI() {
        let json;
        let resultado;
        
        if(buscador.value === ''){
            console.log('buscador: ' + buscador.value);
            json = await fetch(`https://api.themoviedb.org/3/movie/popular?page=${paginaActual}&api_key=aa02e7c79cbe08314c538b9176a77f88&language=es-ES`);
            resultado = await json.json();
            cargarPagina(resultado);
        } else {
            json = await fetch(`https://api.themoviedb.org/3/search/movie?query=${buscador.value}&page=${paginaActual}&api_key=aa02e7c79cbe08314c538b9176a77f88&language=es-ES`);
            resultado = await json.json();
            console.log(resultado);
            cargarPagina(resultado);
        }
    }

    function cargarPagina(resultado){



        while(listaPelis.lastChild) {
            listaPelis.removeChild(listaPelis.firstChild);
        }
        
        for (const pelicula of resultado.results) {
            const peliculaDiv = document.createElement('div');
            peliculaDiv.classList.add('movie-item-style-1');
            peliculaDiv.classList.add('movie-item-style-2');
            peliculaDiv.innerHTML = `
                <img src="https://image.tmdb.org/t/p/w500/${pelicula.poster_path}" alt="">
                <div class="hvr-inner">
                    <a href="/IMDeustoB/peliculas/${pelicula.id}/">Read more</a>
                </div>
                <div class="mv-item-infor">
                    <h6><a href="/IMDeustoB/peliculas/${pelicula.id}/">${pelicula.title}</a></h6>
                </div>
            `;
            listaPelis.append(peliculaDiv);
        }

        
        window.scrollTo(0, 0);
        paginaActualSpan.textContent = resultado.page;
        resulTotal.textContent = resultado.total_results;
        paginaTotalSpan.textContent = resultado.total_pages;
        paginasTotales = parseInt(resultado.total_pages);
    }

    
    botonDerecho.addEventListener('click', async (event) => {
        event.preventDefault(); 
        event.stopPropagation();
        console.log('click derecho');
        
        if(paginaActual < paginasTotales){
            paginaActual++;
            console.log('llamada');
            await llamarAPI();
        }
    });

    botonIzquierdo.addEventListener('click', async (event) => {
        event.preventDefault(); 
        event.stopPropagation();
        console.log('click izquierdo');
        
        if(paginaActual > 1){
            paginaActual--;
            await llamarAPI();
        }
    });

    buscador.addEventListener('keypress', async event => {
        if(event.key === 'Enter'){
            event.preventDefault();
            event.stopPropagation();
            paginaActual = 1;
            
            llamarAPI();
        }
    });
});