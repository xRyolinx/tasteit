// Init page
async function init() {
    // Wait a little because window bugs and doesnt show correctly its innerHeight
    await new Promise(resolve => setTimeout(resolve, 1));

    // Size
    update_height();

    // Delete cover
    document.getElementById('cover').remove();
}

// Update height
function update_height()
{
    // Add back normal size
    let body = document.querySelector('body');
    body.setAttribute("style", "height: " + window.innerHeight.toString() + "px");
}



// Add new message sent
function add_new_msg_sent(parent, dict)
{
    // Create node
    let new_msg = document.createElement('div');
    new_msg.classList.add("msg_sent");

    // Adjust it
    new_msg.id = dict["id"];
    new_msg.innerHTML = '<p class="msg">' + dict['message'] +'</p>';

    // Add it
    parent.append(new_msg);
}

// Add new message received
function add_new_msg_received(parent, dict, username, pdp)
{
    // Create node
    let new_msg = document.createElement('div');
    new_msg.classList.add("msg_received");

    // Adjust it
    new_msg.id = dict["id"];
    new_msg.innerHTML = '<img class="pdp_message" src=' + pdp + ' alt="">' +
                        '<div class="txt_msg">' +
                            '<p class="name_msg">' + username + '</p>' +
                            '<p class="msg">' + dict['message'] +'</p>'+
                        '</div>';

    // Add it
    parent.append(new_msg);
}

// Remove child nodes
function removeChildren(parent) {
    while (parent.firstChild)
    {
        parent.removeChild(parent.firstChild);
    }
}


// Update messages
function update_messages(response)
{
    if (response['status'] == true)
    {
        // data
        response = response['data'];

        // Update chat box
        let messages = document.querySelector('.messages');
        response.forEach(message => {
            // Name and pdp
            let destinataire = document.querySelector('.destinataire');
            let username = destinataire.children[1].children[1].innerHTML;
            let pdp = destinataire.children[1].children[0].src;

            if (message['id_sent'] == destinataire.id)
            {
                add_new_msg_received(messages, message, username, pdp);
            }
            else
            {
                add_new_msg_sent(messages, message);
            }

            formData.set('last_id', message['id']);
        });

        // Scroll
        let msg_container = document.querySelector('.messages_container');
        msg_container.scrollTop = msg_container.scrollHeight;
    }
}

// sleep time expects milliseconds
function sleep(time)
{
    return new Promise((resolve) => setTimeout(resolve, time));
}


// Polling from db
async function polling(formdata) {
    // Fetch
    let result = await fetch('/receive', {
            method : 'post',
            body : formdata,
        });

    // Get response
    result = await result.json();

    // Return
    return result;
}


// stop polling
async function stop_polling()
{
    if (formData.get('id_destinataire') != 0)
    {
        end = true;
        while (end == true)
        {
            await sleep(500);
        }
    }
    formData.set('id_destinataire' , 0);

    console.log('Polling stopped !');
}



// Load Destinataire
function load_destinataire(id) {
    // Person choosen
    let person = document.getElementById(id);

    // Change informations at the top of discussion :
    // id
    let destinataire = document.querySelector('.destinataire');
    destinataire.id = id;
    // pdp
    let pdp = destinataire.children[1].children[0];
    pdp.src = person.children[0].children[0].src;
    // username
    let username = destinataire.children[1].children[1];
    username.innerHTML = person.children[1].children[0].innerHTML;

    // Clear discussion
    removeChildren(document.querySelector('.messages'));
    
    // Change global data
    formData.set('id_destinataire' , id);
    formData.set('last_id', 0);

    // Check if the request was made by phone
    if (window.innerWidth < 800)
    {
        // hide boite
        change_display('.boite', 'none');
        // display messagerie
        change_display('.messagerie', 'flex');
        
        // poll
        console.log('Polling started !');
        short_polling();
    }
}


// Short polling
async function short_polling()
{
    // Update recur
    recur_num++;

    // Wait response
    let result = await polling(formData);

    // There are new messages
    if (result['status'] == true)
    {
        // Update messages
        update_messages(result);
    }
    else
    {
        // Wait a little before fetching again
        await sleep(500);
    }


    // Re-run polling
    if (end == false)
    {
        short_polling();
    }
    
    // End
    recur_num--;
    if (recur_num == 0)
    {
        end = false;
    }
}

function change_display(element, display)
{
    document.querySelector(element).style.display = display;
}



// Global data
let formData = new FormData();
formData.set('id_destinataire' , 0);
formData.set('last_id', 0);


let recur_num = 0;
let end = false;

let resizing = false;


//Start
document.addEventListener('DOMContentLoaded', function() {
    // Go back to messages
    document.getElementById('go_back_discu').addEventListener('click', function() {
        // stop polling
        stop_polling();

        // Change css
        change_display('.messagerie', 'none');
        change_display('.boite', 'flex');
    });

    // initialisation
    init();

    // Get first child for pc
    if (window.innerWidth > 800)
    {
        let first = document.querySelector('.courrier').firstElementChild.id;
        load_destinataire(first);

        // poll
        console.log('Polling started !');
        short_polling();
    }

    // In case of resize
    window.addEventListener('resize', async function() {
        // update height
        update_height();

        // global var of resize
        if (resizing == true)
        {
            return;
        }
        resizing = true;

        // Wait a little
        // await sleep(50);


        // Get current destinataire id
        let id = formData.get('id_destinataire');

        // If there is already an id destinaire
        if (id != 0)
        {
            // turned to phone
            if (window.innerWidth <= 800)
            {
                // hide boite
                change_display('.boite', 'none');
                // display messagerie
                change_display('.messagerie', 'flex');
            }
            // turned to pc
            else
            {
                // hide boite
                change_display('.boite', 'flex');
                // display messagerie
                change_display('.messagerie', 'flex');
            }
        }

        // No destinataire selectionned and turned to pc
        else if (id == 0 && window.innerWidth > 800)
        {
            // Charge the first person
            let first = document.querySelector('.courrier').firstElementChild.id;
            load_destinataire(first);

            // poll
            console.log('Polling started !');
            short_polling();
        }
        // end
        resizing = false;
    })


    
    // Sending message
    let input = document.querySelector('.text_zone');
    let send = document.querySelector('#send');
    
    input.addEventListener('keyup', function(event) {
        if ((event.key == 'Enter') && (input.value != ''))
        {
            send.click();
        }
    });

    send.addEventListener('click', function() {
        // Input blank
        if (input.value == '')
        {
            return;
        }

        // Send message
        let id_destinataire = document.querySelector('.destinataire').id;

        let formData = new FormData();
        formData.set('id_destinataire', id_destinataire);
        formData.set('msg', input.value);
        
        fetch('/send', {
            method : 'post',
            body : formData
        });

        // Input to blank
        input.value = '';
    });
})