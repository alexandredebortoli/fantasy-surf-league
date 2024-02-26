document.addEventListener("DOMContentLoaded", async function () {
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

  // Profile - Predictions
  const selectedEvent = document.getElementById("current-event-select");

  if (selectedEvent) {
    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;
    const dropdownItems = document.querySelectorAll(".event-select");
    const events = await fetchApi("events", csrfToken);
    const predictions = await fetchApi("predictions", csrfToken);
    const surfers = await fetchApi("surfers", csrfToken);

    dropdownItems.forEach((item) => {
      item.addEventListener("click", async function () {
        // Event Dropdown
        selectedEvent.innerText = item.innerText;
        item.classList.add("disabled");
        item.setAttribute("aria-disabled", "true");
        profileDropdownActive(dropdownItems, item);
        // Event Detail
        const currentEventNumber = selectedEvent.innerText.split("#")[1];
        const currentEvent = await getCurrentEvent(
          events,
          currentEventNumber,
          surfers
        );
        if (currentEvent.fields.status === "Completed")
          document
            .getElementById("new-prediction-btn")
            .setAttribute("disabled", "true");
        else
          document
            .getElementById("new-prediction-btn")
            .removeAttribute("disabled");
        await getCurrentEventPrediction(predictions, currentEvent, surfers);
      });
    });
  }

  // Profile - New Prediction Form Not Empty
  const predictionForm = document.getElementById("prediction-form");
  if (predictionForm) {
    predictionForm.addEventListener("submit", function (event) {
      const firstPlace = document.getElementById("first-place-select");
      const secondPlace = document.getElementById("second-place-select");

      if (firstPlace.value == "" || secondPlace.value == "") {
        event.preventDefault();
        alert("Please select both first and second place.");
      }

      if (firstPlace.value == secondPlace.value) {
        event.preventDefault();
        alert("Please select different values for first and second place.");
      }
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

async function getCurrentEvent(events, currentEventNumber, surfers) {
  const currentEvent = await events.find(
    (event) => event.fields.number == currentEventNumber
  );

  if (!currentEvent) {
    alert(`Failed to load selected event`);
    return;
  }

  document
    .getElementById("new-prediction-event")
    .setAttribute("value", currentEvent.pk);

  const eventTitle = document.getElementById("current-event-title");
  const eventLocation = document.getElementById("current-event-location");

  eventTitle.innerHTML = `
  #${currentEvent.fields.number} <b class="me-2">${currentEvent.fields.name}</b>
  <span class="badge ${
    currentEvent.fields.status == "Completed"
      ? "text-bg-primary"
      : currentEvent.fields.status == "Standby"
      ? "text-bg-danger"
      : currentEvent.fields.status == "Live"
      ? "text-bg-warning"
      : "text-bg-secondary"
  } rounded-pill fs-6">${currentEvent.fields.status}</span>
  `;

  eventLocation.innerText = currentEvent.fields.location;

  const toggleBtn = document.getElementById(`toggle-result`);
  if (toggleBtn) {
    toggleBtn.remove();
    document.getElementById(`result-event`).remove();
  }
  const currentEventDiv = document.getElementById("current-event");
  if (
    currentEvent.fields.status === "Completed" &&
    currentEvent.fields.first_place &&
    currentEvent.fields.second_place
  ) {
    const first = surfers.find(
      (surfer) => surfer.pk === currentEvent.fields.first_place
    );
    const second = surfers.find(
      (surfer) => surfer.pk === currentEvent.fields.second_place
    );
    currentEventDiv.innerHTML += `
            <a id="toggle-result" class="btn btn-outline-primary mt-3 show-results"
                data-bs-toggle="collapse" href="#result-event" role="button" aria-expanded="false">
                Show Results
            </a>
            <div class="row collapse mt-4 gap-4" id="result-event">
                <div class="col-xl-12 col-12 d-flex align-items-center gap-3">
                    <i class="bi bi-1-circle text-primary fs-2"></i>
                    <div class="w-100 d-flex align-items-center gap-2">
                        <div class="col-auto">
                            <img class="rounded-circle img-fluid" src="${first.fields.headshot_url}"
                                alt="${first.fields.name}" style="max-width: 64px; max-height: 64px;">
                        </div>
                        <div class="col">
                            ${first.fields.name}
                            <br>
                            <small class="text-secondary-emphasis"><i class="bi bi-geo"></i>
                            ${first.fields.country}</small>
                        </div>
                    </div>
                </div>
                <div class="col d-flex align-items-center gap-3">
                    <i class="bi bi-2-circle text-danger fs-2"></i>
                    <div class="w-100 d-flex align-items-center gap-2">
                        <div class="col-auto">
                            <img class=" rounded-circle img-fluid" src="${second.fields.headshot_url}"
                                alt="${second.fields.name}" style="max-width: 64px; max-height: 64px;">
                        </div>
                        <div class="col">
                        ${second.fields.name}
                            <br>
                            <small class="text-secondary-emphasis"><i class="bi bi-geo"></i>
                            ${second.fields.country}</small>
                        </div>
                    </div>
                </div>
    `;
  }

  return currentEvent;
}

async function getCurrentEventPrediction(predictions, currentEvent, surfers) {
  const currentEventPredictions = predictions.find(
    (prediction) => prediction.fields.event === currentEvent.pk
  );

  const predictionPoints = document.getElementById("prediction-points");
  predictionPoints.innerText = "0 Points";

  if (currentEventPredictions) {
    predictionPoints.innerText = `${currentEventPredictions.fields.points} Points`;

    first = surfers.find(
      (surfer) => surfer.pk === currentEventPredictions.fields.first
    );
    second = surfers.find(
      (surfer) => surfer.pk === currentEventPredictions.fields.second
    );

    document.getElementById("first-prediction").innerHTML = `
      <i class="bi bi-1-square fs-2"></i>
      <img class="img-fluid" src="${first.fields.headshot_url}"
          alt="surfer profile photo" style="max-width: 64px; max-height: 64px;">
      ${first.fields.name}
      <br>
      <small class="text-secondary-emphasis fs-6"><i class="bi bi-geo"></i>${
        first.fields.country
      }</small>
      <i class="bi ${
        currentEvent.fields.status === "Completed"
          ? first.pk == currentEvent.fields.first_place
            ? "bi-check-circle-fill text-success"
            : "bi-x-circle-fill text-danger"
          : "bi-dash-circle-dotted text-secondary"
      } fs-1"></i>
    `;

    document.getElementById("second-prediction").innerHTML = `
      <i class="bi bi-2-square fs-2"></i>
      <img class="img-fluid" src="${second.fields.headshot_url}"
          alt="surfer profile photo" style="max-width: 64px; max-height: 64px;">
      <div>${second.fields.name}</div>
      <br>
      <small class="text-secondary-emphasis fs-6"><i class="bi bi-geo"></i>${
        second.fields.country
      }</small>
      <i class="bi ${
        currentEvent.fields.status === "Completed"
          ? second.pk == currentEvent.fields.second_place
            ? "bi-check-circle-fill text-success"
            : "bi-x-circle-fill text-danger"
          : "bi-dash-circle-dotted text-secondary"
      } fs-1"></i>
    `;
  } else {
    document.getElementById("first-prediction").innerHTML = `
      <i class="bi bi-1-square fs-2"></i>
      <img class="img-fluid" src="${staticUrl}"
          alt="surfer profile photo" style="max-width: 64px; max-height: 64px;">
      --
      <br>
      <small class="text-secondary-emphasis fs-6"><i class="bi bi-geo"></i>--</small>
      <i class="bi bi-dash-circle-dotted text-secondary fs-1"></i>
    `;

    document.getElementById("second-prediction").innerHTML = `
      <i class="bi bi-2-square fs-2"></i>
      <img class="img-fluid" src="${staticUrl}"
          alt="surfer profile photo" style="max-width: 64px; max-height: 64px;">
      --
      <br>
      <small class="text-secondary-emphasis fs-6"><i class="bi bi-geo"></i>--</small>
      <i class="bi bi-dash-circle-dotted text-secondary fs-1"></i>
    `;
  }
}

async function fetchApi(uri, csrfToken) {
  const response = fetch(`http://127.0.0.1:8000/api/${uri}`, {
    method: "GET",
    headers: { "Content-type": "application/json", "X-CSRFToken": csrfToken },
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      }
      throw new Error(`Failed to load predictions`);
    })
    .then((data) => {
      return data;
    })
    .catch((error) => {
      alert(error.message);
    });

  return response;
}
