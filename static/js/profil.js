// Convert a div to a form
function convert_to_form(container)
{
    // Create the form
    let form = document.createElement("form");
    form.classList.add("informations");

    form.id = 'form';
    form.method = 'post';
    form.action = '/update';

    form.addEventListener("submit", function(event) {
        document.querySelector('#save').click();
        event.preventDefault();
    })


    // Insert the children
    container.childNodes.forEach(child => {
        form.append(child.cloneNode(true));
    });

    // Insert the form
    let parent = container.parentElement;
    parent.append(form);

    // Delete the container
    container.remove();
}

// Convert a form to a div
function convert_to_div(form)
{
    // Create the form
    let container = document.createElement("div");
    container.classList.add("informations");

    // Insert the children
    form.childNodes.forEach(child => {
        container.append(child.cloneNode(true));
    });

    // Insert the form
    let parent = form.parentElement;
    parent.append(container);

    // Delete the container
    form.remove();
}





//Start
document.addEventListener('DOMContentLoaded', function() {
    let edit = document.querySelector("#edit");
    let save = document.querySelector("#save");



    // Edit
    edit.addEventListener("click", function() {
        // Convert all the fields
        let spans = document.querySelectorAll(".stat");
        let inputs = document.querySelectorAll(".input");
    
        spans.forEach(span => {
            span.style.display = 'none';
        });
        inputs.forEach(input => {
            input.style.display = 'inline';
        });

        // Convert the container to a form
        let container = document.querySelector('.informations');
        convert_to_form(container);

        // Convert to save
        edit.style.display = 'none';
        save.style.display = 'inline';
    });


    // Save
    save.addEventListener("click", function() {
        // Send to DB


        // Convert all the fields and get values
        let spans = document.querySelectorAll(".stat");
        let inputs = document.querySelectorAll(".input");
        let values = [];
    
        inputs.forEach(input => {
            input.style.display = 'none';
            values.push(input.value);
        });

        let i = 0;
        spans.forEach(span => {
            span.innerHTML = values[i];
            span.style.display = 'inline';
            i++;
        });
        

        // Convert the form to a container
        let form = document.querySelector('.informations');
        convert_to_div(form);


        // Convert to save
        edit.style.display = 'inline';
        save.style.display = 'none';
    });
});