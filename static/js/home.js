// Update mode and size
function update_mode() 
{
    // Update previous mode
    prev_mode = mode;

    // Save sizes and states
    let div = document.querySelector('#hauteur_div');
    let size = div.clientHeight - window.innerHeight;
    console.log('size : ', size);

    // If not in navigateur
    if (size < 0)
    {
        return;
    }

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
function update_height()
{
    // Update mode
    update_mode();

    // Add back class
    let main = document.querySelector('main');
    main.setAttribute("style", "height: 92vh");

    // Get current height
    let new_size = main.clientHeight;

    // Delete height of url in portrait
    if ((prev_mode == 'large' && mode == 'long') || (prev_mode == 'none'))
    {
        new_size -= size_url;
        main.setAttribute("style", "height: " + new_size.toString() + 'px');
        console.log('size decreased : ' + size_url.toString());
    }
    // Add back height of url in paysage
    else if (prev_mode == 'long' && mode == 'large')
    {   
        new_size += size_url;
        main.style.height = new_size.toString() + 'px';
        console.log('size increased : ' + size_url.toString());
    }
}


// Global var
let prev_mode = 'none';
let mode = 'none';
let size_url = 0;


//Start
document.addEventListener('DOMContentLoaded', function() {
    // Size
    update_height();

    // Rotation
    window.addEventListener('resize', () => {
        update_height();
    });
});