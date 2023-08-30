var current_slider_image_index = 0
var slider_image_index_identifiers = document.getElementsByClassName("slider_indexes")[0].getElementsByTagName("p")
var slider = document.getElementsByClassName("sliders")[0]
var slider_imgs = slider.getElementsByClassName("slider");

function _slider_move() {
	slider_imgs[1].className = "slider"

	var temp = slider_imgs[0]
	slider.removeChild(slider_imgs[0])
	slider.appendChild(temp)

	slider_imgs[1].removeEventListener("transitionend", _slider_move)

	slider_image_index_identifiers[current_slider_image_index].className = "identifier"
    current_slider_image_index += 1

	if (slider_image_index_identifiers.length == current_slider_image_index) {
	    current_slider_image_index = 0
	}

	slider_image_index_identifiers[current_slider_image_index].className = "identifier active"
}

function slider_move() {
    slider_imgs[1].className = "slider slider_move"
	slider_imgs[1].addEventListener("transitionend", _slider_move);
}

setInterval(slider_move, 3800)