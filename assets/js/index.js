const registerForm = $("#register-form");
// let txtCustomerId = $("#cust_id");
let txtCustomerName = $("#name");
let txtCustomerEmail = $("#email");
let txtCustomerAddress = $("#address");
let txtCustomerContact = $("#contact");

let baseURL = "http://localhost:5000";
let recSystemUrl = "http://localhost:8501/";

function clearForm() {
  // txtCustomerId.val("");
  txtCustomerName.val("");
  txtCustomerAddress.val("");
  txtCustomerEmail.val("");
  txtCustomerContact.val("");
}

function saveCustomer() {
  $.ajax({
    url: baseURL + "/save",
    method: "POST",
    data: $("#register-form").serialize(),
    success: function (resp) {
      console.log(resp);
      if (resp.status === 201) {
        console.log("success.........");
        alert(resp.message);
        clearForm();
        window.location.href = recSystemUrl;
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

$("#btn_register").click(function (e) {
  console.log("saving.......");
  const data = {
    name: txtCustomerName.val(),
    address: txtCustomerAddress.val(),
    email: txtCustomerEmail.val(),
    contact: txtCustomerContact.val(),
  };
  console.log(data);
  console.log($("#register-form").serialize());

  saveCustomer();
});
