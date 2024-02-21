document.addEventListener("DOMContentLoaded", function () {
  // Set the theme according to user preference
  const prefersLightScheme = window.matchMedia("(prefers-color-scheme: light)");

  if (prefersLightScheme.matches) {
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
      link.classList.add("fw-bold");
      link.setAttribute("aria-current", "page");
    } else {
      link.classList.remove("active");
      link.classList.remove("fw-bold");
      link.removeAttribute("aria-current");
    }
  });

  // Events Page - Show/Hide the event results
  const showResults = document.querySelectorAll(".show-results");
  if (showResults) {
    showResults.forEach((btn) => {
      btn.addEventListener("click", function () {
        if (btn.getAttribute("aria-expanded") === "true") {
          btn.classList.remove("btn-outline-primary");
          btn.classList.add("btn-outline-danger");
          btn.innerHTML = "Hide Results";
        } else {
          btn.classList.add("btn-outline-primary");
          btn.classList.remove("btn-outline-danger");
          btn.innerHTML = "Show Results";
        }
      });
    });
  }
});
