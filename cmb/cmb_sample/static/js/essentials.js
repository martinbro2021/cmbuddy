function openSidebarMenu() {
  document.getElementById("cmb-menu-sidebar").style.width = "100%";
  document.getElementById("cmb-menu-sidebar").style.display = "block";
}

function closeSidebarMenu() {
  document.getElementById("cmb-menu-sidebar").style.display = "none";
}

function setAccents() {
  const topBar = document.getElementById("cmb-menu-topbar").getElementsByClassName("cmb-menu-item");
  const sideBar = document.getElementById("cmb-menu-sidebar").getElementsByClassName("cmb-menu-item");
  for (let item of [...topBar, ...sideBar]) {
    if (item.href.replaceAll("/", "") == window.location.href.replaceAll("/", "")) {
      item.classList.add("cmb-accent");
    }
  }
}

function init() {
  setAccents();
}

document.addEventListener("DOMContentLoaded", init);
