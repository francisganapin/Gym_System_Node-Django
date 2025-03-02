

  document.querySelectorAll(".dropbtn").forEach((button) => {
    button.addEventListener("click", function () {
      // Close all dropdowns before opening the clicked one
      document.querySelectorAll(".dropdown-content").forEach((dropdown) => {
        if (dropdown !== this.nextElementSibling) {
          dropdown.classList.add("hidden");
        }
      });

      // Toggle only the related dropdown
      this.nextElementSibling.classList.toggle("hidden");
    });
  });

  // Close dropdown when clicking outside
  document.addEventListener("click", function (event) {
    if (!event.target.closest(".relative")) {
      document.querySelectorAll(".dropdown-content").forEach((dropdown) => {
        dropdown.classList.add("hidden");
      });
    }
  });

