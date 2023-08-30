products_app = Vue.createApp({
    data() {
        return {
            products: [],
            actionable_element_is_in_action: false,
        }
    },
    methods: {
        get_products(GetProductsRequestSchema) {
            ProductServices.get_products(GetProductsRequestSchema)
        },
        update_product_is_favourite_field(product) {
            if (product.is_favourite) {
                UserServices.add_products_to_favourites([product.id])
            } else {
                UserServices.remove_product_from_favourites(product.id)
            }
        },
        open_product_page(product) {
            if (!this.actionable_element_is_in_action) {
                window.location.href = '/product/?product_id=' + product.id
            }
        },
        actionable_element_mouse_over() {
            this.actionable_element_is_in_action = true

        },
        actionable_element_mouse_out() {
            this.actionable_element_is_in_action = false

        },
    }
})

products_app.config.compilerOptions.delimiters = ["${", "}"];
mounted_products_app = products_app.mount("#products_app")
