//----------functions-----------//

// PS : 'query' is passed from html file

// Ajouter elements
async function add_el(template, add) {
    // BDD de plats
    response = await fetch("/restaurants_list?id=" + id + "&n=" + add + query);
    let plats = await response.json();

    // Select DOM
    let main = document.querySelector('main');
    let id_min = 0;

    // Add
    for (let i in plats)
    {
        // Clone
        let element = template.cloneNode(true);
        
        // Modify
        // Image
        if (!(plats[i]['photo'] == ''))
        {
            let img = element.children[0].children[0];
            img.src = "data:;base64," + plats[i]['photo'];
        }
        
        // Description
        let el_txt = element.children[1].children[1];

        // Nom
        let nom = el_txt.children[0];
        nom.innerHTML = plats[i]["name"];
        // Adress
        let restau = el_txt.children[1];
        restau.innerHTML = plats[i]["adress"];
        // Rating
        let rating = el_txt.children[2].children[0];
        rating.innerHTML = plats[i]["rating"] + "%";

        // ID
        let id = el_txt.children[2].children[1];
        id.value = plats[i]["id"];


        // Insert
        main.append(element);

        // Mise a jour de id_min
        id_min = parseInt(plats[i]["id"]);
    }

    // Update id
    if (id_min != 0)
    {
        id = id_min;
    }

    // last id
    if (id == last_id)
    {
        let seemore = document.querySelector(".seemore");
        seemore.remove();
    }
}

//-----------------------------//

// Last id
async function last_async() {
    let response = await fetch("/restaurants_list?t=0" + query);
    last_id = await response.json();
}

//-----------------------------//

//Global starting elements
let nb_elements = 8;
let add_element = 4;
let id = 0;
let last_id = 0;


//Start
document.addEventListener('DOMContentLoaded', async function() {
    // Last id
    await last_async();

    //Starting element of global
    if ((window.matchMedia("(max-width: 1024px)").matches))
    {
        nb_elements = 2;
        add_element = 3;
    }

    //Save template
    let element = document.querySelector('.element');
    let copy = element.cloneNode(true);
    copy.style.display = 'block';

    // Delete template
    element.remove();

    // Add elements
    add_el(copy, nb_elements);

    //Voir plus
    document.querySelector('#plus').addEventListener('click', function(event){
        add_el(copy, add_element);
        event.preventDefault();
    });
});