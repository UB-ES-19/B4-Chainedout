
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

$(document)
    .one('focus.autoExpand', 'textarea.autoExpand', function(){
        var savedValue = this.value;
        this.value = '';
        this.baseScrollHeight = this.scrollHeight;
        this.value = savedValue;
    })
    .on('input.autoExpand', 'textarea.autoExpand', function(){
        var minRows = this.getAttribute('data-min-rows')|0, rows;
        this.rows = minRows;
        rows = Math.ceil((this.scrollHeight - this.baseScrollHeight) / 16);
        this.rows = minRows + rows;
    });

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

// CAROUSEL
    function plusSlides(n) {
        showSlides(slideIndex += n);
    }

    function currentSlide(n) {
        showSlides(slideIndex = n);
    }

    function showSlides(n) {
        var i;
        var slides = document.getElementsByClassName("mySlides_carousel");
        var dots = document.getElementsByClassName("dot_carousel");
        if (n > slides.length) {
            slideIndex = 1
        }
        if (n < 1) {
            slideIndex = slides.length
        }
        for (i = 0; i < slides.length; i++) {
            slides[i].style.display = "none";
        }
        for (i = 0; i < dots.length; i++) {
            dots[i].className = dots[i].className.replace(" active", "");
        }
        slides[slideIndex - 1].style.display = "block";
        dots[slideIndex - 1].className += " active";
    }