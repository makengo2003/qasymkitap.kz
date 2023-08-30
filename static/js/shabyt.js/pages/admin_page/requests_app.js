requests_app = Vue.createApp({
    data() {
        return {
            requests: [],
            current_section: "books",
            there_are_new_requests: {
                books: false,
                languages: false,
                certificates: false,
            }
        }
    },
    methods: {
        open() {
            this.open_section()

        },
        open_section() {
            axios.get(`/api/request/get_requests/?category=${this.current_section}`).then((response) => {
                this.requests = response.data
            })
        },
        close() {},
        window_scroll_down_event_listener() {},
        accept_request(request) {
            axios.post("/api/request/accept_request/" + request.id + "/", {}, {
                headers: {
                    "X-CSRFToken": $cookies.get("csrftoken"),
                }
            }).then((response) => {
                request.is_accepted = true
            })
        },
        check_new_requests() {
            axios.get("/api/request/check_new_requests/").then((response) => {
                this.there_are_new_requests = response.data
            })
        }
    },
    mounted() {
        this.check_new_requests()
        setInterval(this.check_new_requests, 3000)
    }
})


requests_app.config.compilerOptions.delimiters = ["${", "}"];
mounted_requests_app = requests_app.mount("#requests")
