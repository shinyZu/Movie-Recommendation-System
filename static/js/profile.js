console.log("====================================");
console.log("Profile Loaded");
console.log("====================================");

function loadImage(event) {
  var image = document.getElementById("preview-image");
  image.style.display = "block";
  image.src = URL.createObjectURL(event.target.files[0]);
}

const form = document.getElementById("profile-form");
const preview = document.getElementById("preview");
const fileInput = document.getElementById("profile-pic");

fileInput.addEventListener("change", function () {
  const file = this.files[0];
  if (file) {
    const reader = new FileReader();
    reader.addEventListener("load", function () {
      preview.src = reader.result;
    });
    reader.readAsDataURL(file);
  }
});

form.addEventListener("submit", function (event) {
  event.preventDefault();
  const data = new FormData(form);
  fetch("/update_profile", {
    method: "POST",
    body: data,
  })
    .then((response) => response.json())
    .then((data) => {
      alert(data.message);
    })
    .catch((error) => {
      console.error(error);
      alert("There was an error updating your profile.");
    });
});
