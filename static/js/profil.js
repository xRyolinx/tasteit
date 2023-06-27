// Convert a div to a form
function convert_to_form(container)
{
    // Create the form
    let form = document.createElement("form");
    form.classList.add("informations");
    form.id = 'form';
    // When submit, simulate a click on save
    form.addEventListener("submit", function(event) {
        document.querySelector('#save').click();
        event.preventDefault();
    })


    // Insert the children
    for(let i = 0 ; i < container.children.length;)
    {
        form.appendChild(container.children[i]);
    }

    // Insert the form
    let parent = container.parentElement;
    parent.appendChild(form);

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
    for(let i = 0 ; i < form.children.length;)
    {
        container.appendChild(form.children[i]);
    }

    // Insert the div
    let parent = form.parentElement;
    parent.appendChild(container);

    // Delete the form
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
    save.addEventListener("click", async function() {
        // Send to DB
        let form = document.querySelector('.informations');
        
        // Grab the data inside the form fields
        const formData = new FormData(form);
        
        // Fetch
        let response = await fetch('/profil', {   
            method: 'POST',
            body: formData,
        });

        // What the server sent back as dict
        let result = await response.json();

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

        // Update username
        console.log(result);
        if (result['check'] == false)
        {
            // Input
            document.querySelector('#username').value = result['value'];
            // Div
            document.querySelector('#username').parentElement.firstChild.innerHTML = result['value'];
        }
        

        // Convert the form to a container
        convert_to_div(form);


        // Convert to save
        edit.style.display = 'inline';
        save.style.display = 'none';
    });
});