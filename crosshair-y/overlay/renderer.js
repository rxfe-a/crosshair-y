const box = document.getElementById("imgBox");
let visible = true;

window.overlayAPI.onToggle(() => {
  visible = !visible;
  box.style.display = visible ? "block" : "none";
});
