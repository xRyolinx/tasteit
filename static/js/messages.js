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
    while (parent.firstChild) {
        parent.removeChild(parent.firstChild);
    }
}

// Load Destinataire
function load_destinataire(id) {
    let person = document.getElementById(id);

    // Change informations at the top of discussion
    // id
    let destinataire = document.querySelector('.destinataire');
    destinataire.id = id;
    // pdp
    let pdp = destinataire.children[0].children[0];
    pdp.src = person.children[0].children[0].src;
    // username
    let username = destinataire.children[0].children[1];
    username.innerHTML = person.children[1].children[0].innerHTML;

    // Clear discussion
    removeChildren(document.querySelector('.messages'));
    
    // Change global data
    formData.set('id_destinataire' , id);
    formData.set('last_id', 0);
}


// 1. Call helloCatAsync passing a callback function,
//    which will be called receiving the result from the async operation


// Long polling
async function polling() {
    // socket.connect();
    // socket.emit("receive", id_destinataire, last_id);
    let response = await fetch('/receive', {
        method : 'post',
        body : formData
    })
    response = await response.json();

    console.log(response);

    // Get response
    let last_id = 0;
    if (response['status'] == true)
    {
        // data
        response = response['data'];
        // Update chat box
        let messages = document.querySelector('.messages');
        response.forEach(message => {
            // Name and pdp
            let destinataire = document.querySelector('.destinataire');
            let username = destinataire.children[0].children[1].innerHTML;
            let pdp = destinataire.children[0].children[0].src;

            if (message['id_sent'] == destinataire.id)
            {
                add_new_msg_received(messages, message, username, pdp);
            }
            else
            {
                add_new_msg_sent(messages, message);
            }

            last_id = message['id'];
        });

        // Scroll
        let msg_container = document.querySelector('.messages_container');
        msg_container.scrollTop = msg_container.scrollHeight;
    }

    // Return
    return last_id;
}


// Global data
let formData = new FormData();
formData.set('id_destinataire' , 0);
formData.set('last_id', 0);


//Start
document.addEventListener('DOMContentLoaded', function() {
    // Web socket
    // const socket = io({autoConnect: false});

    // Get first child
    let first = document.querySelector('.courrier').firstElementChild.id;
    load_destinataire(first);

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

        // Connect to websocket
        // socket.connect();

        // Send message
        let id_destinataire = document.querySelector('.destinataire').id;

        let formData = new FormData();
        formData.set('id_destinataire', id_destinataire);
        formData.set('msg', input.value);
        
        fetch('/send', {
            method : 'post',
            body : formData
        });

        // socket.emit("send", input.value, id_destinataire);

        // Input to blank
        input.value = '';
    });


    // Long polling
    setInterval(function() {
        polling().then(function(result) {
            // update last id
            if (result != 0)
            {
                formData.set('last_id', result);
            }
            console.log(formData.get('last_id'));
            
        });
    }, 1000);
    
    

    // Get response
    // socket.on('receive', function(data) {
        
    // });

})