var dataContainer = $("#book_cards")
var selects = document.getElementsByTagName("select")
var pagination_container = $('#pagination')

var urlParams = new URLSearchParams(window.location.search);
var current_page_number = urlParams.get("page")
var category = urlParams.get("category")
var order_by = urlParams.get("order_by")
var query = [category, order_by]

function set_url_params(param_name, param_value) {
    var currentURL = window.location.href;
    var urlParams = new URLSearchParams(window.location.search);

    urlParams.set(param_name, param_value);
    var newURL = currentURL.split('?')[0] + '?' + urlParams.toString();
    window.history.pushState({ path: newURL }, '', newURL);
}

function set_pagination() {
    var book_cards = document.getElementsByClassName("book_card")
    var books = []

    for (var i = 0; i < book_cards.length; i++) {
        books.push({"html": book_cards[i]})
    }

    $.extend($.fn.pagination.defaults, {
        pageSize: 3,
        dataSource: books,
    })

    pagination_container.pagination({
        dataSource: books,
        pageSize: 5,
        callback: function(data, pagination) {
            set_url_params("page", pagination["pageNumber"])
            dataContainer.html(template(data))
        }
    })

    pagination_container.pagination(current_page_number)

    pagination_container.pagination("destroy")
}

function template(data) {
    var books_template = ""

    for (var i = 0; i < data.length; i++) {
        books_template += data[i]["html"].outerHTML
    }

    return books_template
}

function set_books(event) {
    if (event.target.id == "book_category") {
        category = event.target.options[event.target.selectedIndex].value
        set_url_params("category", category)
    } else {
        order_by = event.target.options[event.target.selectedIndex].value
        set_url_params("order_by", order_by)
    }

    current_page_number = 1
    get_book_cards()
}

for (var i = 0; i < selects.length; i++) {
    selects[i].onchange = (event) => {
        set_books(event)
    }

    for (var j = 0; j < selects[i].options.length; j++) {
        if (selects[i].options[j].value === query[i]) {
            selects[i].selectedIndex = j;
            break;
        }
    }
}

function get_book_cards() {
    axios.get(`/book_cards/`, {
        params: {
            products_filtration: JSON.stringify({category: category}),
            order_by: order_by
        }
    }).then((response) => {
        document.getElementById("books").innerHTML = JSON.parse(response["data"])["html"]
        set_pagination()
    })
}

get_book_cards()