// Wait for DOM to load
window.addEventListener("DOMContentLoaded", _ => {

    // Listen for the user clicking the submit button on the form
    document.getElementById('form_submit').addEventListener('click', _ => {

        let form = document.getElementById('document_form');
        let fd = new FormData(form);

        let arg_text = fd.get('document_text');

        if (arg_text.length > 0) {
            const canaryEndpoint = "/canary/api/v1/analyse";
            fetch(canaryEndpoint, {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body:
                    JSON.stringify({document_text: arg_text})
            }).then(res => res.text().then(hash => window.location.href = `/view/job/${hash}`))
        }
    });

    // Listen for the user uploading a file
    document.getElementById('text_file').addEventListener('change', () => {
        let form = document.getElementById('document_form');
        let fd = new FormData(form);

        let text_file = fd.get('text_file');
        if (text_file.size > 0) {
            // user has upload a text file instead. Read it and send to Canary
            let fileReader = new FileReader();
            fileReader.onload = (() => {
                document.getElementById('document_text').innerHTML = fileReader.result;
            })
            fileReader.readAsText(text_file, "utf-8")
        }
    });
});
