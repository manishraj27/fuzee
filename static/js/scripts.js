const navMenu = document.querySelector(".nav_menu"),
    ToggleBtn = document.querySelector(".toggle_btn"),
    CloseBtn = document.querySelector(".close_btn");

// ==== SHOW MENU ==== //
ToggleBtn.addEventListener("click", () => {
    navMenu.classList.add("show");
    document.querySelector("body").classList.add("no-scroll");
});

// ==== HIDE MENU ==== //
CloseBtn.addEventListener("click", () => {
    navMenu.classList.remove("show");
    document.querySelector("body").classList.remove("no-scroll");
});

gsap.from(".logo", {
    opacity: 0,
    y: 10,
    delay: 1,
    duration: 0.5,
});
// ==== NAV-MENU ==== //
gsap.from("ul li", {
    opacity: 0,
    y: 10,
    delay: 1.4,
    duration: 0.5,
    stagger: 0.3,
});
// ==== TOGGLE BTN ==== //
gsap.from(".toggle_btn", {
    opacity: 0,
    y: 10,
    delay: 1.2,
    duration: 0.5,
});

// ==== FLEX ITEM ==== //
gsap.from(".flex-item-1", {
    opacity: 0,
    y: 20,
    delay: 2.8,
    duration: 1,
});

// ====  IMAGE ==== //
gsap.from(".tagline", {
    opacity: 0,
    y: 20,
    delay: 3,
    duration: 1,
});