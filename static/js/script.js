document.addEventListener("DOMContentLoaded", function () {
  const menuBtn = document.querySelector(".menu-btn");
  const navbarItems = document.querySelector(".navbar-items");

  menuBtn.addEventListener("click", () => {
    navbarItems.classList.toggle("show");
  });
});


// document.getElementById('test').innerHTML = "hi mony"
