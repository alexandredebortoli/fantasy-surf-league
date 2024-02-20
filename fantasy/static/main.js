document.addEventListener("DOMContentLoaded", function () {
  var path = window.location.pathname.substring(1);

  var navLinks = document.querySelectorAll(".nav-link");
  navLinks.forEach((link) => {
    var href = link.innerHTML.toLowerCase();

    if (
      (href === "home" && path === "") ||
      (href === "log in" && path === "login") ||
      (href === "register" && path === "register")
    ) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    } else {
      link.classList.remove("active");
      link.removeAttribute("aria-current");
    }
  });
});
