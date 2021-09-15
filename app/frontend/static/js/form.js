window.addEventListener("DOMContentLoaded", _ => {

    document.getElementById('form_submit').addEventListener('click', e => {

        let form = document.getElementById('document_form');
        let fd = new FormData(form);

        let arg_text = fd.get('document_text');
        let text_file = fd.get('text_file');

        const canaryEndpoint = "/canary/api/v1/analyse";

        if (arg_text.length > 0) {
            console.log("doin")
            fetch(canaryEndpoint, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body:
                    JSON.stringify({document_text: arg_text})
            }).then(res => res.text().then(console.log))

        } else if (text_file > 0) {

        } else {
            alert("...");
        }
    });
});
