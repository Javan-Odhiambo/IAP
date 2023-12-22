const sidebar = document.querySelector("#sidebar");
const closeButton = document.querySelector("#sidebar-close");

closeButton.addEventListener("click", () => {
  sidebar.style.left = "-16rem";
  console.log('Close button clicked, sidebar should be hidden.');
});

document.querySelector("#hambugger").addEventListener("click", (e) => {
  e.stopPropagation();
  sidebar.style.left = "0";
  console.log('Hambugger clicked, sidebar should be visible.');
});

document.addEventListener("click", (event) => {
  if (
    !event.target.closest("#sidebar") &&
    !event.target.matches("#hambugger")
  ) {
    sidebar.style.left = "-16rem";
    console.log('Clicked outside sidebar, sidebar should be hidden.');
  }
});

document.querySelector("#profile-icon").addEventListener("click", (e) => {
    const profileOptions = document.querySelector("#profile-options");
    profileOptions.classList.toggle("show");
  });