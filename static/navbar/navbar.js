//------------------- functions -----------------------//

//Initialize navbar en fonction de window
function show_hide_nav()
{
    //Hide - Show
    let nav = document.querySelector('nav');
    let nav_add = document.querySelector('#nav_add');
    let nav_button = document.querySelector('#nav_button');

    // Hide add on mobile
    if (window.matchMedia("(max-width: 992px)").matches)
    {
        nav.after(nav_add);
        nav_add.style.display = 'none';
        nav_button.style.display = 'block';
    }
    // Hide button on pc
    else
    {
        nav_button.before(nav_add);
        nav_add.style.display = 'flex';
        nav_button.style.display = 'none';
    }
}

//Changer couleur de bordure top/bot
function nav_element_color(element, color) {
    // element.style.borderTopColor = color;
    element.style.borderBottomColor = color;    
    element.style.color = '#264653';
}

// Couleur du link de la page actuelle, dans nav
function nav_element_page(color) {
    let window_path_name = window.location.pathname;
    // Home page
    if ((window_path_name == '/') || (window_path_name == '/index.html'))
    {
        nav_home = document.querySelector('#nav_home');
        nav_element_color(nav_home, color);
        nav_home.style.fontWeight = 'bold';
    }
    // Autre pages
    pages = document.querySelectorAll('.nav_el');
    pages.forEach(page => {
        if ((window_path_name.includes(page.innerHTML.replace(' ', '').toLowerCase()))
        && page.id != 'nav_home')
        {
            nav_element_color(page, color);
            page.style.fontWeight = 'bold';
        }    
    });
}

//Change la couleur du link de la page actuelle
function adapt_element_page_size()
{
    // Mobile
    if (window.matchMedia("(max-width: 992px)").matches)
    {
        nav_element_page('transparent');
    }
    // PC
    else
    {
        nav_element_page('#264653');
    }
}

// Reset la page
function nav_resize() {
    show_hide_nav();
    adapt_element_page_size();
}
// --------------------------------------------------- //


//Start
let nav_bar_counter = 0;
document.addEventListener('DOMContentLoaded', function() {
    //Initialize navbar
    nav_resize();

    //Nav button in mobile
    let nav_button = document.querySelector('#nav_button');
    nav_button.addEventListener('click', function() {
        let nav = document.querySelector('nav');
        let nav_add = document.querySelector('#nav_add');
        //Show
        if (nav_bar_counter % 2 == 0)
        {
            //Suite de navbar
            nav_add.style.display = 'flex';
            nav_bar_counter++;
        }
        // Hide
        else
        {
            nav_add.style.display = 'none';
            nav_bar_counter++;
        }
    });

    //Reset la page
    window.addEventListener('resize', nav_resize);
});