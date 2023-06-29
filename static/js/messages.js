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

// Error message
function error_msg(id, msg)
{
    document.querySelector(id).parentElement.parentElement.children[2].innerHTML = msg;
}

// PDP : From Edit to Save/Cancel
function pdp_edit_to_changes()
{
    let changes_pdp = document.querySelector('#changes_pdp');
    changes_pdp.style.display = 'flex';

    let edit_pdp = document.querySelector('#label_edit_pdp');
    edit_pdp.style.display = 'none';

    let pdp_and_buttons = document.querySelector('.pdp_and_buttons');
    pdp_and_buttons.style.position = 'relative'
    let pdp_container = document.querySelector('.pdp_container');
    pdp_container.style.position = 'absolute';
    let img_container = document.querySelector('.img_container');
    img_container.style.position = 'static';
}

// PDP : From Changes to Edit
function pdp_changes_to_edit()
{
    let changes_pdp = document.querySelector('#changes_pdp');
    changes_pdp.style.display = 'none';

    let edit_pdp = document.querySelector('#label_edit_pdp');
    edit_pdp.style.display = 'flex';

    let pdp_and_buttons = document.querySelector('.pdp_and_buttons');
    pdp_and_buttons.style.position = 'static'
    let pdp_container = document.querySelector('.pdp_container');
    pdp_container.style.position = 'relative';
    let img_container = document.querySelector('.img_container');
    img_container.style.position = 'absolute';
}



//Start
document.addEventListener('DOMContentLoaded', function() {
    // Scroll
    let msg_container = document.querySelector('.messages_container');

    msg_container.scrollTop = msg_container.scrollHeight;
});