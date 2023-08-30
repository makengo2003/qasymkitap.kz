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



function open_certificates_request_form() {
    document.getElementById('request-form').style.display = 'block';
    document.getElementById('request-form-category').value = 'certificates'
}

function open_languages_request_form(language) {
    document.getElementById('request-form').style.display = 'block';
    document.getElementById('request-form-category').value = 'languages'
    document.getElementById('request-form-language').value = language
}

document.getElementById("request-form").onsubmit = (event) => {
    event.preventDefault()

    axios.post('/api/request/leave_request/', {
        category: document.getElementById('request-form-category').value,
        fullname: document.getElementById('request-form-fullname').value,
        phone_number: document.getElementById('request-form-phone_number').value,
        request_text: document.getElementById('request-form-language').value,
    }, {
        headers: {
            "X-CSRFToken": $cookies.get("csrftoken"),
        }
    }).then((response) => {
        alert("Қабылданды, жауапты күтіңіз")
        close_request_form()
    })
}