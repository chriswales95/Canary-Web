function postText(text) {
    const canaryEndpoint = "/canary/api/v1/analyse";

    fetch(canaryEndpoint, {
        method: "POST",
        headers: {
            'Content-Type': 'application/json'
        },
        body:
            JSON.stringify({document_text: text})
    }).then(res => res.text().then(hash => window.location.href = `/view/job/${hash}`))
}

window.addEventListener("DOMContentLoaded", _ => {

    document.getElementById('form_submit').addEventListener('click', e => {

        let form = document.getElementById('document_form');
        let fd = new FormData(form);

        let arg_text = fd.get('document_text');

        if (arg_text.length > 0) {
            postText(arg_text);
        }
    });

    document.getElementById('text_file').addEventListener('change', () => {
        let form = document.getElementById('document_form');
        let fd = new FormData(form);

        let text_file = fd.get('text_file');
        if (text_file.size > 0) {
            // user has upload a text file instead. Read it and send to Canary
            let fileReader = new FileReader();
            fileReader.onload = (() => {
                console.log('///')
                document.getElementById('document_text').innerText = fileReader.result;
            })
            fileReader.readAsText(text_file)
        }
    });
});

