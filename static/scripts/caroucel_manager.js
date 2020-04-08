
function caroucel_press(elem) {
	var activated = document.getElementsByClassName('active'); //lis
	for (var i = 0; i < activated.length; i++) {
		activated[i].classList.remove("active");
	}

	activated = document.getElementsByClassName('activated'); //
	for (var i = 0; i < activated.length; i++) {
		activated[i].classList.add("deactivated");
		activated[i].classList.remove("activated");
	}

	document.getElementById(elem.getAttribute("for")).classList.add("activated");
	document.getElementById(elem.getAttribute("for")).classList.remove("deactivated");
	
	elem.classList.add("active");
}