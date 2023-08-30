var wishlist = localStorage.getItem("wishlist")

if (wishlist) {
    axios.get(`/book_cards/`, {
        params: {
            products_filtration: JSON.stringify({id__in: JSON.parse(wishlist)})
        }
    }).then((response) => {
        document.getElementById("books").innerHTML = JSON.parse(response["data"])["html"]
    })
}
