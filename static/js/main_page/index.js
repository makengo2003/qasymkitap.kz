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
        sweetalert("Қабылданды, бірнеше минут ішінде менеджерлер хабарласады")
        close_request_form()
    })
}