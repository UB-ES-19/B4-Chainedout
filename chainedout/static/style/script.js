
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
	var modals = [document.getElementById('login_modal'), 
	document.getElementById('profile_modal'),
	document.getElementById('about_modal'), 
	document.getElementById('xp_modal'),
	document.getElementById('skills_modal'), 
	document.getElementById('achievements_modal')];
	
	for (i = 0; i < modals.length; i++) {
		if (event.target == modals[i]) {
			modals[i].style.display = "none";
		}
	}
}

// shows/hides modal
function modal(id, type) {
	var modal = document.getElementById(id);
	modal.style.display = type;
}