const registerForm = $("#register-form");
// let txtCustomerId = $("#cust_id");
let txtCustomerName = $("#name");
let txtCustomerEmail = $("#email");
let txtCustomerPwd = $("#pwd");
let txtCustomerAddress = $("#address");
let txtCustomerContact = $("#contact");

let baseURL = "http://localhost:5000";

function clearForm() {
  // txtCustomerId.val("");
  txtCustomerName.val("");
  txtCustomerAddress.val("");
  txtCustomerEmail.val("");
  txtCustomerPwd.val("");
  txtCustomerContact.val("");
}

// ================================Register/SignUp=================================

function saveCustomer() {
  $.ajax({
    url: "/save",
    method: "POST",
    data: $("#register-form").serialize(),
    success: function (resp) {
      console.log(resp);
      if (resp.status === 201) {
        console.log("success.........");
        // alert(resp.message);
        // Swal.fire({
        //   icon: "success",
        //   title: "",
        //   showConfirmButton: true,
        //   footer: `<a href="">${resp.message}</a>`,
        // });
        clearForm();
        window.location.href = "/movies/home";
      } else {
        console.log("error................");
        // alert(resp.message);
        Swal.fire({
          icon: "error",
          title: "Failed to sign up.",
          showConfirmButton: false,
          footer: `<a href="">${resp.message}</a>`,
        });
      }
    },
    error: function (ob, textStatus, error) {
      console.log("server side error................");
      console.log(ob);
    },
  });
}

$("#btn_register").click(function (e) {
  console.log("saving.......");
  const data = {
    name: txtCustomerName.val(),
    address: txtCustomerAddress.val(),
    email: txtCustomerEmail.val(),
    pwd: txtCustomerPwd.val(),
    contact: txtCustomerContact.val(),
  };
  console.log(data);
  console.log($("#register-form").serialize());

  saveCustomer();
});

// ================================Login/SignIn=====================================

function loginCustomer(custObj) {
  $.ajax({
    url: "/login",
    method: "POST",
    contentType: "application/json",
    data: JSON.stringify(custObj),
    success: function (resp) {
      console.log(resp);

      if (resp.status === 200) {
        console.log("success.........");
        window.location.href = "/movies/home";
      } else {
        console.log("error................");
        // alert(resp.message);
        Swal.fire({
          icon: "error",
          title: "Failed to sign in.",
          showConfirmButton: false,
          footer: `<a href="">${resp.message}</a>`,
        });
      }
    },
    error: function (ob, textStatus, error) {
      console.log("server side error................");
      console.log(ob);
    },
  });
}

$("#btn_login").click(function (e) {
  console.log("clicked login.......");
  const data = {
    email: txtCustomerEmail.val(),
    pwd: txtCustomerPwd.val(),
  };
  console.log(data);
  loginCustomer(data);
});
