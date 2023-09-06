cart_app = Vue.createApp({
    data() {
        return {
            cart_items: [],
        }
    },
    methods: {
        _buy_request_form_submit(event) {
            event.preventDefault()
            var cart_items = []

            for (var i = 0; i < this.cart_items.length; i++) {
                cart_items.push({
                    "book_name": this.cart_items[i]["book"]["name"],
                    "count": this.cart_items[i]["count"],
                    "book_id": this.cart_items[i]["book"]["id"]
                })
            }

            axios.post('/api/request/leave_request/', {
                category: "books",
                fullname: document.getElementById('request-form-fullname').value,
                phone_number: document.getElementById('request-form-phone_number').value,
                cart_items: cart_items
            }, {
                headers: {
                    "X-CSRFToken": $cookies.get("csrftoken"),
                }
            }).then((response) => {
                sweetalert("Қабылданды, бірнеше минут ішінде менеджерлер хабарласады")
                close_request_form()
                localStorage.removeItem("cart")
                window.location.href = "/"
            })
        },
        buy() {
            document.getElementById("request-form").style.display = "block"
            document.getElementById('request-form-category').value = "books"

            document.getElementById("request-form").getElementsByTagName("form")[0].onsubmit = this._buy_request_form_submit
        },
        delete_cart_item(cart_item) {
            this.cart_items.splice(this.cart_items.indexOf(cart_item), 1)
            this.update_cart_items_count()
        },
        update_cart_items_count() {
            var cart_items = []

            for (var i = 0; i < this.cart_items.length; i++) {
                cart_items.push({"book_id": this.cart_items[i].book.id, "count": this.cart_items[i].count})
            }

            localStorage.setItem("cart", JSON.stringify(cart_items))
        },
        cart_item_total_price(cart_item) {
            return Number(cart_item["book"]["price"]) * Number(cart_item["count"])

        },
        total_books_count() {
            var books_count = 0

            for (var i = 0; i < this.cart_items.length; i++) {
                books_count += Number(this.cart_items[i]["count"])
            }

            return books_count
        },
        total_price() {
            var price = 0

            for (var i = 0; i < this.cart_items.length; i++) {
                price += Number(this.cart_items[i]["book"]["price"]) * Number(this.cart_items[i]["count"])
            }

            return price
        },
    },
    mounted() {
        var cart_ls = localStorage.getItem("cart")

        if (cart_ls) {
            var cart = JSON.parse(cart_ls)
            var book_ids = []

            for (var i = 0; i < cart.length; i++) {
                book_ids.push(cart[i]["book_id"])
            }

            axios.get("/api/product/get_products/", {
                params: {
                    products_filtration: JSON.stringify({id__in: book_ids})
                }
            }).then((response) => {
                this.cart_items = []

                for (var i = 0; i < response.data.length; i++) {
                    this.cart_items.push({
                        book: {
                            id: response.data[i]["id"],
                            name: response.data[i]["name"],
                            price: response.data[i]["price"],
                            poster: response.data[i]["poster"],
                        },
                        count: cart[i]["count"]
                    })
                }
            })
        }
    }
})

cart_app.config.compilerOptions.delimiters = ["${", "}"];
mounted_cart_app = cart_app.mount("#cart_app")
