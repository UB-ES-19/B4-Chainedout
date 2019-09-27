
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  var modal = document.getElementById('login_modal');
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

// shows/hides navigation menu
function loginModal(id, type) {
    var modal = document.getElementById(id);
    modal.style.display = type;
}