console.log("====================================");
console.log("movie js");
console.log("====================================");

// let baseURL = "http://localhost:5000";
// let server_path_for_movie_titles = "/movies";

const movie_container = $("#card_main_container");
const dropDown = $("#cmb_movies");

let movieTitles = [];
let recommendedMovies = [];
let recommendedMoviePosters = [];
var selectedOption;
let cardsData = [];

let img_size = "450x500";

let profile_tab = $("#0");
let customer_id = 0;

// Get the Id of the logged customer
// getCustomerId();

(function () {
  console.log("profle tab id");
  console.log(profile_tab.attr("id"));

  var loggedUserId = JSON.parse(sessionStorage.getItem("loggedUserId"));
  console.log("loggedUserId: " + loggedUserId);

  profile_tab.attr("id", loggedUserId);
  console.log(profile_tab.attr("id"));
})();

// Load drop down list
loadMovieTitlesForCmb();

// Generate and append cards to the DOM
generateCards("Avatar");

function getCustomerId() {
  console.log("movies - getting cutomer id............");
  console.log(profile_tab.attr("id"));

  $.ajax({
    url: "/getId",
    method: "GET",
    success: function (resp) {
      console.log(resp);

      if (resp.status === 200) {
        customer_id = resp.lastId;
        console.log("success.........");
        profile_tab.attr("id", customer_id);
        console.log(profile_tab.attr("id"));
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

    card.addEventListener("mouseover", function () {
      card.style.border = "3px inset #1abc9c";
      card.style.cursor = "pointer";
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

    // img.style.border = "2px solid yellow";
    // cardContainer.style.border = "2px solid red";
    // currentRow.style.border = "2px solid blue";
    // cardCol.style.border = "2px solid #fff";
    // card.style.border = "2px solid yellow";
    // cardBody.style.border = "2px solid pink";
  });
}

function getRecommendations(movie_selected) {
  $.ajax({
    url: "/recommendations/" + movie_selected,
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
    // url: baseURL + server_path_for_movie_titles,
    url: "/movies",
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
