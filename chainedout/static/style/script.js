
// When the user clicks anywhere outside of the modal, close it
window.addEventListener("click", function(event) {
	var modals = [
	document.getElementById('login_modal'), 
	document.getElementById('profile_user_edit_modal'),
	document.getElementById('profile_about_modal'),
	document.getElementById('profile_edu_add_modal'),
	document.getElementById('profile_edu_edit_modal'),
	document.getElementById('profile_xp_add_modal'),
	document.getElementById('profile_xp_edit_modal'),
	document.getElementById('profile_skills_add_modal'),
	document.getElementById('profile_skills_edit_modal'), 
	document.getElementById('profile_achievement_modal')
	];
	
	for (i = 0; i < modals.length; i++) {
		if (event.target === modals[i]) {
			modals[i].style.display = "none";
		}
	}
});

// shows/hides modal
function modal(id, type) {
	var modal = document.getElementById(id);
	modal.style.display = type;
}