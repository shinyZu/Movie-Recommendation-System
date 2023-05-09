console.log("====================================");
console.log("navbar js");
console.log("====================================");

// $("#a_movie_hive").click(function (e) {
//   window.location.href = "/movies/home";
// });

// $("#a_profile").click(function (e) {
//   window.location.href = "/profile";
// });

$("#tab_logout").click(function (e) {
  Swal.fire({
    text: "Are you sure you want to Logout..?",
    icon: "question",
    showCancelButton: true,
    confirmButtonText: "Logout",
    confirmButtonColor: "#3498db",
    customClass: {
      cancelButton: "order-1 right-gap",
      confirmButton: "order-2",
    },
    allowOutsideClick: false,
    returnFocus: false,
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.href = "/";
    }
  });
});
