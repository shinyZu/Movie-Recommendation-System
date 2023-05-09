// import { getCustomerId } from "../js/server_index";

// function loadImage(event) {
//   var image = document.getElementById("preview-image");
//   image.style.display = "block";
//   image.src = URL.createObjectURL(event.target.files[0]);
// }

// const form = document.getElementById("profile-form");
// const preview = document.getElementById("preview");
// const fileInput = document.getElementById("profile-pic");

// fileInput.addEventListener("change", function () {
//   const file = this.files[0];
//   if (file) {
//     const reader = new FileReader();
//     reader.addEventListener("load", function () {
//       preview.src = reader.result;
//     });
//     reader.readAsDataURL(file);
//   }
// });

// form.addEventListener("submit", function (event) {
//   event.preventDefault();
//   const data = new FormData(form);
//   fetch("/update_profile", {
//     method: "POST",
//     body: data,
//   })
//     .then((response) => response.json())
//     .then((data) => {
//       alert(data.message);
//     })
//     .catch((error) => {
//       console.error(error);
//       alert("There was an error updating your profile.");
//     });
// });

console.log("====================================");
console.log("Profile Loaded");
console.log("====================================");

let profile_tab = $("#0");
let txtCustId = $("#id");
let txtCustName = $("#name");
let txtCustAddress = $("#address");
let txtCustEmail = $("#email");
let txtCustPwd = $("#pwd");
let txtCustContact = $("#contact");

let customer_id = 0;

// Get the Id of the logged customer
getCustomerId();

if (customer_id != 0) {
  console.log("1 loading......");
  loadProfileData(customer_id);
} else {
  console.log("2 loading......");
}

function getCustomerId() {
  console.log("profile - getting cutomer id............");

  $.ajax({
    url: "/getId",
    method: "GET",
    async: false,
    success: function (resp) {
      console.log(resp);

      if (resp.status === 200) {
        console.log("success.........");
        customer_id = resp.lastId;
        txtCustId.val(customer_id);
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

function loadProfileData(id) {
  console.log("loading profile..of user with id: " + id);

  $.ajax({
    url: baseURL + "/search/" + id,
    method: "GET",
    success: function (resp) {
      console.log(resp.customer);
      let customer = resp.customer;

      if (resp.status === 200) {
        console.log("success.........");

        txtCustName.val(customer.name);
        txtCustAddress.val(customer.address);
        txtCustEmail.val(customer.email);
        txtCustPwd.val(customer.password);
        txtCustContact.val(customer.contact);
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

function updateCustomer(custObj) {
  console.log(custObj);
  $.ajax({
    url: "/update",
    method: "PUT",
    contentType: "application/json",
    data: JSON.stringify(custObj),
    // data: $("#profile_form").serialize(),

    success: function (resp) {
      console.log(resp);

      if (resp.status === 200) {
        console.log("success.........");
        // alert(resp.message);
        Swal.fire({
          icon: "success",
          title: "Profile updated successfully!",
          showConfirmButton: false,
          footer: "\n",
        });

        loadProfileData(custObj.id);
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

$("#btnCancel").click(function (e) {
  console.log("clicked cancel.......");
  window.location.href = "/movies/home";
});

$("#btnSaveChanges").click(function (e) {
  console.log("save changes.......");
  console.log(typeof parseInt(profile_tab.attr("id")));
  console.log(customer_id);
  const data = {
    id: parseInt(txtCustId.val()),
    name: txtCustName.val(),
    email: txtCustEmail.val(),
    pwd: txtCustPwd.val(),
    address: txtCustAddress.val(),
    contact: txtCustContact.val(),
  };
  console.log(data);
  console.log($("#profile_form").serialize());

  Swal.fire({
    text: "Are you sure you want to proceed?",
    icon: "question",
    showCancelButton: true,
    confirmButtonText: "Update",
    confirmButtonColor: "#3498db",
    customClass: {
      cancelButton: "order-1 right-gap",
      confirmButton: "order-2",
    },
    allowOutsideClick: false,
    returnFocus: false,
  }).then((result) => {
    if (result.isConfirmed) {
      updateCustomer(data);
    }
  });
});
