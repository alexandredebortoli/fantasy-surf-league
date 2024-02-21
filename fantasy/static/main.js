document.addEventListener("DOMContentLoaded", function () {
  // Set the theme according to user preference
  const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");

  if (!prefersDarkScheme.matches) {
    document.querySelector("html").setAttribute("data-bs-theme", "light");
  } else {
    document.querySelector("html").setAttribute("data-bs-theme", "dark");
  }

  // Set the active link in the navbar
  var path = window.location.pathname.substring(1);

  var navLinks = document.querySelectorAll(".nav-link");
  navLinks.forEach((link) => {
    var href = link.innerHTML.toLowerCase();

    if (
      (href === "home" && path === "") ||
      (href === "log in" && path === "login") ||
      (href === "register" && path === "register") ||
      (href === "schedule" && path === "schedule")
    ) {
      link.classList.add("active");
      link.setAttribute("aria-current", "page");
    } else {
      link.classList.remove("active");
      link.removeAttribute("aria-current");
    }
  });
});
