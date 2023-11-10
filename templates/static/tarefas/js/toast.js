;(function () {
    const toastElement = document.getElementById("toast")
    const toastBody = document.getElementById("toast-body")
    const toast = new bootstrap.Toast(toastElement, { delay: 2000 })

    htmx.on("showMessage", (e) => {
        toastBody.innerText = e.detail.value
        toast.show()
    })

    const toastMessage = document.getElementById('toastMsg')
    const toastMsg = new bootstrap.Toast(toastMessage, { delay: 3000 })
    toastMsg.show()
})()