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
    let parent = document.querySelector("#informations_container");
    parent.prepend(form);

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
    parent.prepend(container);

    // Delete the form
    form.remove();
}

// Error message
function error_msg(id, msg)
{
    let status = document.querySelector(id).parentElement.parentElement.children[2];
    status.innerHTML = msg;
    console.log(msg);

    if (msg == '')
    {
        status.style.display = "none";
    }
    else
    {
        status.style.display = "inline";
    }
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


// Update mode and size
function update_mode() 
{
    // Update previous mode
    prev_mode = mode;

    // Save sizes and states
    let div = document.querySelector('#hauteur_div');
    let size = div.clientHeight - window.innerHeight;

    // Portrait
    if (window.innerHeight > window.innerWidth)
    {
        mode = 'long';
        size_url = size;
    }
    // Paysage
    else
    {
        mode = 'large';
    }
}

// Update height
function hide_url()
{
    // Update mode
    update_mode();

    // Get current height
    let contenu = document.querySelector('.contenu');
    let new_size = contenu.clientHeight;

    // Delete height of url in portrait
    if ((prev_mode == 'large' && mode == 'long') || (prev_mode == 'none'))
    {
        new_size -= size_url;
        contenu.style.height = new_size.toString() + 'px';
    }
    // Add back height of url in paysage
    else if (prev_mode == 'long' && mode == 'large')
    {   
        new_size += size_url;
        contenu.style.height = new_size.toString() + 'px';
    }

    // if (contenu.clientHeight - size > 450)
    // {
    //     size = contenu.clientHeight - size;
    //     contenu.style.height = size.toString() + 'px';
    // }
}


// Global var
let prev_mode = 'none';
let mode = 'none';

let size_url = 0;


//Start
document.addEventListener('DOMContentLoaded', function() {
    // Size   
    hide_url();
    window.addEventListener('resize', hide_url);
    
    // Vars
    let edit = document.querySelector("#edit");
    let changes = document.querySelector("#changes");
    let save = document.querySelector("#save");
    let save_mob = document.querySelector("#save_mob");
    
    let cancel = document.querySelector("#cancel");
    

    // Edit info
    edit.addEventListener("click", function() {
        // Initialise error messages
        error_msg('#username', '');

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

        // Convert to changes
        edit.style.display = 'none';
        changes.style.display = 'flex';

        if ((window.matchMedia("(max-width: 750px)").matches))
        {
            save_mob.style.display = 'block';
        }
    });


    // Save info
    save_mob.addEventListener("click", function() { save.click() });
    save.addEventListener("click", async function() {
        let check = false;
        // check 3 fields
        let username = document.querySelector('#username').value;
        let email = document.querySelector('#email').value;
        let password = document.querySelector('#password').value;
        if (username == '')
        {
            error_msg('#username', "Username can't be empty");
            check = true;
        }
        if (email == '')
        {
            error_msg('#email', "Email can't be empty");
            check = true;
        }
        if (password == '')
        {
            error_msg('#password', "Password can't be empty");
            check = true;
        }
        if (check == true)
        {
            return;
        }
        else
        {
            error_msg('#username', "");
            error_msg('#email', "");
            error_msg('#password', "");
        }


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

        // Get current username in div
        let current_username = document.querySelector('#username').parentElement.children[0].innerHTML;


        // Convert all the fields and get values of input
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
        if (result['check'] == false)
        {
            // Input
            document.querySelector('#username').value = result['value'];
            // Div
            document.querySelector('#username').parentElement.children[0].innerHTML = result['value'];
            // Error msg
            if (values[0] != current_username)
            {
                error_msg('#username', 'Username already used');
            }
        }
        

        // Convert the form to a container
        convert_to_div(form);


        // Convert to edit
        edit.style.display = 'inline';
        changes.style.display = 'none';
        save_mob.style.display = 'none';
    });


    // Cancel info
    cancel.addEventListener("click", function() {
        // Reset error msg
        error_msg('#username', '');
        error_msg('#email', '');
        error_msg('#password', '');


        // Reset input values and convert to div
        let spans = document.querySelectorAll(".stat");
        let inputs = document.querySelectorAll(".input");
        let values = [];
    
        spans.forEach(span => {
            values.push(span.innerHTML);
            span.style.display = 'inline';
        });

        let i = 0;
        inputs.forEach(input => {
            input.value = values[i];
            input.style.display = 'none';
            i++;
        });


        // Convert the form to a container
        convert_to_div(form);

        // Convert button to edit
        edit.style.display = 'inline';
        changes.style.display = 'none';
        save_mob.style.display = 'none';
    });




    // Edit PDP
    let pdp = document.querySelector('#pdp');
    pdp.addEventListener('change', function() {
        // Change buttons
        pdp_edit_to_changes();

        // Change pdp display
        let pdp_display = document.querySelector('.pdp');
        pdp_display.src = URL.createObjectURL(pdp.files[0]);
    });


    // Save PDP
    let save_pdp = document.querySelector('#save_pdp');
    save_pdp.addEventListener('click', async function() {
        // Send file
        let formData = new FormData();
        formData.append('pdp', pdp.files[0]);
        formData.append('id', document.querySelector('#id').value);
        

        let response = await fetch('/profil', {   
            method: 'POST',
            body: formData,
        });
        response = await response.json();
        console.log(response);

        // Change pdp in nav bar
        let nav_pdp = document.querySelector('.nav_pdp');
        nav_pdp.src = URL.createObjectURL(pdp.files[0]);


        // Change buttons
        pdp_changes_to_edit();
    });


    // Cancel PDP
    let current_pdp = document.querySelector('.pdp').src;
    let cancel_pdp = document.querySelector('#cancel_pdp');
    cancel_pdp.addEventListener('click', function() {
        // Change back display
        document.querySelector('.pdp').src = current_pdp;

        // Change buttons
        pdp_changes_to_edit();
    });
});