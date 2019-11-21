
// When the user clicks anywhere outside of the modal, close it
window.addEventListener("click", function(event) {
	var modals = [
	document.getElementById('login_modal'), 
	document.getElementById('profile_user_edit_modal'),
	document.getElementById('profile_about_modal'),
	document.getElementById('profile_edu_modal'),
	document.getElementById('profile_xp_modal'),
	document.getElementById('profile_skills_modal'),
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

// show post history
function post_histo(id, btn) {
	if (id.style.display !== 'none') {
		id.style.display = 'none';
		btn.innerHTML = "<i class=\"fas fa-search-plus\"></i> Show</div>";
	} else {
		id.style.display = 'block';
		btn.innerHTML = "<i class=\"fas fa-search-minus\"></i> Hide</div>";
	}
}