function open_burger() {
    document.getElementsByClassName("burger")[0].style.display = "flex"
    document.getElementsByClassName("hamburger-menu")[0].src = "/static/imgs/x.png"
    document.getElementsByClassName("hamburger-menu")[0].onclick = close_burger
}

function close_burger() {
    document.getElementsByClassName("burger")[0].style.display = "none"
    document.getElementsByClassName("hamburger-menu")[0].src = "/static/imgs/hamburger.png"
    document.getElementsByClassName("hamburger-menu")[0].onclick = open_burger
}

function disable_a(book_id) {
    document.getElementById("book_" + book_id).removeAttribute("href")

}

function enable_a(book_id) {
    document.getElementById("book_" + book_id).href = "/book/" + book_id + "/"

}

function buy_book(book_id, count=1) {
    document.getElementById("leave_request_window").style.display = "block"
    document.getElementById("leave_request_window-book_id").value = book_id

    document.getElementById("leave_request_window-book_poster").style.backgroundImage = document.getElementById("book_" + book_id).getElementsByClassName("book_img")[0].style.backgroundImage
    document.getElementById("leave_request_window-book_name").innerHTML = document.getElementById("book_" + book_id).getElementsByClassName("book_name")[0].innerHTML
    document.getElementById("leave_request_window-book_category").innerHTML = document.getElementById("book_" + book_id).getElementsByClassName("book_category")[0].innerHTML
    document.getElementById("leave_request_window").getElementsByClassName("book_count")[0].value = count
    document.getElementById("leave_request_window-book_price").getElementsByTagName("span")[0].innerHTML = document.getElementById("book_" + book_id).getElementsByClassName("book_price")[0].getElementsByTagName("span")[0].innerHTML

    handle_request_form_book_count()
}

function close_request_form() {
    document.getElementById('request-form').style.display = 'none';
    document.getElementById('leave_request_window').style.display = 'none';
}

function handle_request_form_book_count() {
    document.getElementById("leave_request_window-sum_price").innerHTML = Number(document.getElementById("leave_request_window").getElementsByClassName("book_count")[0].value) * Number(document.getElementById("leave_request_window-book_price").getElementsByTagName("span")[0].innerHTML)

}

function add_to_cart(book_id, count=1) {
    var cart_ls = localStorage.getItem("cart")

    if (cart_ls) {
        var cart = JSON.parse(cart_ls)
        found = false

        for (var i = 0; i < cart.length; i++) {
            if (cart[i]["book_id"] == book_id) {
                found = true
                break
            }
        }

        if (!found) {
            cart.push({"book_id": book_id, "count": count})
            localStorage.setItem("cart", JSON.stringify(cart))
        }
    }
    else {
        localStorage.setItem("cart", JSON.stringify([{"book_id": book_id, "count": count}]))
    }

    sweetalert("Себетке салынды")
}

function book_in_wishlist(book_id) {
    var wishlist = localStorage.getItem('wishlist')

    if (wishlist) {
        var wishlist = JSON.parse(wishlist)

        if (wishlist.indexOf(book_id) != -1) {
            wishlist.splice(wishlist.indexOf(book_id), 1)
            document.getElementById("book_" + book_id).getElementsByClassName("wishlist_btn")[0].src = "/static/imgs/heart.png"
        }
        else {
            wishlist.push(book_id)
            document.getElementById("book_" + book_id).getElementsByClassName("wishlist_btn")[0].src = "/static/imgs/heart2.png"
        }

        localStorage.setItem("wishlist", JSON.stringify(wishlist))
    } else {
        localStorage.setItem("wishlist", JSON.stringify([book_id]))
    }
}

function check_book_in_wishlist(book_id) {
    var wishlist = localStorage.getItem('wishlist')

    if (wishlist) {
        var wishlist = JSON.parse(wishlist);

        if (wishlist.indexOf(book_id) == -1) {
            document.getElementById("book_" + book_id).getElementsByClassName("wishlist_btn")[0].src = "/static/imgs/heart.png"
        } else {
            document.getElementById("book_" + book_id).getElementsByClassName("wishlist_btn")[0].src = "/static/imgs/heart2.png"
        }
    }
}

function leave_request_window_submit(event) {
    event.preventDefault()

    axios.post('/api/request/leave_request/', {
        category: "books",
        fullname: document.getElementById('leave_request_window-fullname').value,
        phone_number: document.getElementById('leave_request_window-phone_number').value,
        cart_items: [{
            "book_name": document.getElementById("leave_request_window-book_name").innerHTML,
            "count": document.getElementById("leave_request_window").getElementsByClassName("book_count")[0].value,
            "book_id": document.getElementById("leave_request_window-book_id").value
        }]
    }, {
        headers: {
            "X-CSRFToken": $cookies.get("csrftoken"),
        }
    }).then((response) => {
        sweetalert("Қабылданды, бірнеше минут ішінде менеджерлер хабарласады")
        close_request_form()
    })
}

function sweetalert(title) {
    Swal.fire(
      'Qasym kitaphanasy',
      title,
      'success'
    )
}
