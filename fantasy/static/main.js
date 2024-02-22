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
      (href === "events" && path === "events") ||
      (href === "rankings" && path === "rankings") ||
      (href === "surfers" && path === "surfers") ||
      (href === "league" && path === "league") ||
      (href.includes("@") && path.includes("profile"))
    ) {
      link.classList.add("active");
      if (!href.includes("@")) link.classList.add("fw-bold");
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

  // Join League Code Input
  const leagueId = document.getElementById("league-identifier");
  if (leagueId) {
    leagueId.addEventListener("keydown", function (event) {
      if (event.key === "Enter") {
        event.preventDefault();
      }
    });
    leagueId.addEventListener("input", function () {
      var inputLength = this.value.length;
      if (inputLength === 11) {
        document.getElementById("join-btn").classList.remove("d-none");
      } else {
        document.getElementById("join-btn").classList.add("d-none");
      }
    });
  }

  // Profile - Event Selection Dropdown
  const currentEvent = document.getElementById("current-event-select");

  if (currentEvent) {
    const dropdownItems = document.querySelectorAll(".event-select");

    dropdownItems.forEach((item) => {
      item.addEventListener("click", function () {
        currentEvent.innerText = item.innerText;
        item.classList.add("disabled");
        item.setAttribute("aria-disabled", "true");
        profileDropdownActive(dropdownItems, item);
      });
    });
  }
});

function profileDropdownActive(dropdownItems, activeItem) {
  dropdownItems.forEach((item) => {
    if (item === activeItem) return;

    item.classList.remove("disabled");
    item.removeAttribute("aria-disabled");
  });
}
