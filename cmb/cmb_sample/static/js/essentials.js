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
    if (item.href && window.location.href.replaceAll("/", "").includes(item.href.replaceAll("/", ""))) {
      item.classList.add("cmb-accent");
    }
  }
}

function randomizeNthChild() {
  const calendarEntries = document.getElementById("cmb-calendar-entries");
  if (calendarEntries) {
    for (let i = 0; i < Math.random() * 13; i++) {
      calendarEntries.prepend(document.createElement("span"));
    }
  }
}

function init() {
  setAccents();
  randomizeNthChild();
}

document.addEventListener("DOMContentLoaded", init);
