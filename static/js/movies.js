console.log("movies......");

let baseURL = "http://localhost:5000";

const movie_container = $("#card_main_container");
const dropDown = $("#cmb_movies");

let movieTitles = [];
let recommendedMovies = [];
let recommendedMoviePosters = [];
var selectedOption;
let cardsData = [];

let img_size = "450x500";

// Sample card data
// const cardsData = [
//   {
//     imgSrc: "https://via.placeholder.com/" + img_size,
//     title: "Card 1",
//     text: "Some quick example text to build on the card title and make up the bulk of the card's content.",
//     caption: "Caption goes here",
//   },
//   {
//     imgSrc: "https://via.placeholder.com/" + img_size,
//     title: "Card 2",
//     text: "Some quick example text to build on the card title and make up the bulk of the card's content.",
//     caption: "Caption goes here",
//   },
//   {
//     imgSrc: "https://via.placeholder.com/" + img_size,
//     title: "Card 3",
//     text: "Some quick example text to build on the card title and make up the bulk of the card's content.",
//     caption: "Caption goes here",
//   },
//   {
//     imgSrc: "https://via.placeholder.com/" + img_size,
//     title: "Card 4",
//     text: "Some quick example text to build on the card title and make up the bulk of the card's content.",
//     caption: "Caption goes here",
//   },
//   {
//     imgSrc: "https://via.placeholder.com/" + img_size,
//     title: "Card 5",
//     text: "Some quick example text to build on the card title and make up the bulk of the card's content.",
//     caption: "Caption goes here",
//   },
//   {
//     imgSrc: "https://via.placeholder.com/" + img_size,
//     title: "Card 6",
//     text: "Some quick example text to build on the card title and make up the bulk of the card's content.",
//     caption: "Caption goes here",
//   },
// ];

// ------

// (function () {

// })();

// Load drop down list

loadMovieTitlesForCmb();
generateCards("Avatar");

// Function to generate and append cards to the DOM
function generateCards(movie_title) {
  const cardContainer = document.getElementById("card_main_container");
  getRecommendations(movie_title);
  console.log(cardsData);

  let currentRow = null;

  console.log(cardContainer.childElementCount);
  if (cardContainer.childElementCount != 0) {
    console.log("removing children");
    // cardContainer.removeChild(cardContainer.childNodes);
    cardContainer.innerHTML = "";
  }

  // Loop through the card data and generate card elements
  cardsData.forEach((cardData, index) => {
    // Create a new row every 3 cards
    if (index % 3 === 0) {
      currentRow = document.createElement("div");
      currentRow.classList.add("row");
      cardContainer.appendChild(currentRow);
    }

    const cardCol = document.createElement("div");
    cardCol.classList.add("col-md-4", "mb-4");

    const card = document.createElement("div");
    card.classList.add("card");
    card.style.border = "none";
    card.style.borderBottomLeftRadius = "22px";
    card.style.borderBottomRightRadius = "22px";

    const img = document.createElement("img");
    img.classList.add("card-img-top");
    img.src = cardData.imgSrc;
    img.alt = cardData.title;
    card.appendChild(img);

    var initialHeight = img.clientHeight;
    card.addEventListener("mouseover", function () {
      // card.style.border = "5px inset #16a085";
      card.style.border = "3px inset #1abc9c";
    });
    card.addEventListener("mouseout", function () {
      card.style.border = "none";
    });

    const cardBody = document.createElement("div");
    cardBody.classList.add("card-body");
    cardBody.style.backgroundColor = "#343a40";

    const cardTitle = document.createElement("h5");
    cardTitle.classList.add("card-title");
    cardTitle.textContent = cardData.title;
    cardBody.appendChild(cardTitle);
    cardBody.style.color = "#fff";
    cardBody.style.borderBottomLeftRadius = "20px";
    cardBody.style.borderBottomRightRadius = "20px";

    card.appendChild(cardBody);

    cardCol.appendChild(card);
    currentRow.appendChild(cardCol);
  });
}

function getRecommendations(movie_selected) {
  $.ajax({
    url: baseURL + "/recommendations/" + movie_selected,
    method: "GET",
    async: false,
    success: function (resp) {
      console.log(resp);

      if (resp.status === 200) {
        console.log("success.........");
        recommendedMovies = resp.movieList;
        recommendedMoviePosters = resp.posterList;

        // console.log(recommendedMovies);
        // console.log(recommendedMoviePosters);

        let x = [];
        for (let i = 0; i < recommendedMovies.length; i++) {
          let card_obj = {
            imgSrc: recommendedMoviePosters[i],
            title: recommendedMovies[i],
          };
          //   card_obj.imgSrc = recommendedMoviePosters[i] + "/" + img_size;
          //   card_obj.title = recommendedMovies[i];
          x.push(card_obj);
        }
        cardsData = x;
      } else {
        console.log("error................");
        alert(resp.message);
      }
    },
    error: function (ob, textStatus, error) {
      console.log("server side error................");
      console.log(ob);
    },
  });
}

function loadMovieTitlesForCmb() {
  $.ajax({
    url: baseURL + "/movies",
    method: "GET",
    // async: false,
    success: function (resp) {
      console.log(resp);

      if (resp.status === 200) {
        console.log("success.........");
        movieTitles = JSON.parse(resp.titleList);

        // console.log(movieTitles);

        var select = document.getElementById("cmb_movies");

        for (var i = 0; i < movieTitles.length; i++) {
          var option = document.createElement("option");

          option.value = i;
          option.textContent = movieTitles[i];
          select.appendChild(option);
        }
      } else {
        console.log("error................");
        alert(resp.message);
      }
    },
    error: function (ob, textStatus, error) {
      console.log("server side error................");
      console.log(ob);
    },
  });
}

function recomendMovies() {}

$("#cmb_movies").click(function (e) {
  console.log("selected.......");

  var selectElement = document.getElementById("cmb_movies");
  var selectedIndex = selectElement.selectedIndex;
  selectedOption = selectElement.options[selectedIndex];
  console.log(selectedOption.value);
});

$("#btn_recommend").click(function (e) {
  console.log("clicked.......");
  for (var i = 0; i < movieTitles.length; i++) {
    if (i == selectedOption.value) {
      movie_selected = movieTitles[i];
      generateCards(movie_selected);
    }
  }
});
