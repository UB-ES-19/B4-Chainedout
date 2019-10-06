
// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
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
	document.getElementById('profile_publication_modal'),
	document.getElementById('profile_patent_modal'),
	document.getElementById('profile_course_modal'),
	document.getElementById('profile_project_modal'),
	document.getElementById('profile_awards_modal'),
	document.getElementById('profile_test_q_modal'),
	document.getElementById('profile_lang_modal'),
	document.getElementById('profile_company_modal')
	];
	
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