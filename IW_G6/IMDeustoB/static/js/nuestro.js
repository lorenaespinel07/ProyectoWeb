document.addEventListener('DOMContentLoaded', () => {
    let paginaActual = 1

    const botonIzquierdo = document.querySelector('.pagination2 .ion-arrow-left-b');
    const botonDerecho = document.querySelector('.pagination2 .ion-arrow-right-b');
    const listaPelis = document.querySelector('.flex-wrap-movielist');
    const paginaActualSpan = document.querySelector('.pagination2 span span');

    async function cargarPagina(){
        console.log('pagina' + paginaActual);
        json = await fetch(`https://api.themoviedb.org/3/movie/popular?page=${paginaActual}&api_key=aa02e7c79cbe08314c538b9176a77f88&language=es-ES`);
        resultado = await json.json();
        console.log(resultado.results);

        while(listaPelis.lastChild) {
            listaPelis.removeChild(listaPelis.firstChild);
        }

        

        for (const pelicula of resultado.results) {


            const peliculaDiv = document.createElement('Div');
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
        console.log(paginaActualSpan)
        paginaActualSpan.textContent = resultado.page;

        



    }

    botonDerecho.addEventListener('click', (event) => {
        console.log('click');
        event.preventDefault();
        event.stopPropagation();
        paginaActual++;
        cargarPagina();
    })

    botonIzquierdo.addEventListener('click', (event) => {
        event.preventDefault();
        event.stopPropagation();
        if(paginaActual !== 1){
            paginaActual--;
            cargarPagina();
        }
    })
})
