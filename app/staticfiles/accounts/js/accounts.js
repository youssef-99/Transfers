addEventListener("DOMContentLoaded", (event) => {
    let model = new Modal()
});

class Modal {
    constructor() {
        this.init()
    }

    modal = null

    createModal() {
        this.modal = new bootstrap.Modal(document.getElementById('uploadModal'));
        this.form = document.getElementById('uploadForm');
        this.validateForm()
    }


    validateForm() {


        this.form.addEventListener('submit',  (event) => {
            console.log(this.form)
            event.preventDefault();
            let fileInput = document.getElementById('accountFile');

            let file = fileInput.files[0];
            if (!file.name.toLowerCase().endsWith('.csv')) {
                let errorMessageElement = document.getElementById('error-message');
                errorMessageElement.innerText = 'File must be a CSV file.';
            } else {
                this.form.submit();
            }
        });
    }

    init() {
        this.createModal()
    }
}
