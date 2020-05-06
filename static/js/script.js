
const actors = document.getElementsByClassName('actors');


for (let actor of actors) {
    actor.addEventListener('click', function (event) {
        event.target.nextElementSibling.classList.toggle("hide");
    })
}


let genres = document.getElementsByClassName('genres')


for (let genre of genres) {
    let arrayOfGenres = genre.innerText.split(',');
    genre.innerHTML = "";
    for (let genreArray of arrayOfGenres) {
        genreArray = genreArray.trim();
        genreArray = `<a href="/shows-by-genre/${genreArray}">${genreArray}</a>`
        genre.innerHTML += genreArray;
        console.log(genre)
    }
}

