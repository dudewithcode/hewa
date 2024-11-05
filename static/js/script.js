let btn = document.querySelector("#btn");
let sidebar = document.querySelector(".sidebar");

btn.onclick = function () {
  sidebar.classList.toggle("active");
};

// Show the popover if there’s an error message
document.addEventListener("DOMContentLoaded", function () {
  const error = "{{ error }}";
  if (error) {
    document.getElementById("errorPopover").style.display = "block";
    document.getElementById("overlay").style.display = "block";
  }
});

function closePopover() {
  document.getElementById("errorPopover").style.display = "none";
  document.getElementById("overlay").style.display = "none";
}
