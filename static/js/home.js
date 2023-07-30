// Update mode and size
function update_mode() 
{
    // Update previous mode
    prev_mode = mode;

    // Save sizes and states
    let div = document.querySelector('#hauteur_div');
    let size = div.clientHeight - window.innerHeight;
    alert(
        'height: ' + window.innerHeight.toString() + ' | 100vh = ' + div.clientHeight.toString() +
        ' | size url = ' + size.toString()
    );

    // If not in navigateur
    if (size < 0)
    {
        return 0;
    }

    // Portrait
    if (window.innerHeight > window.innerWidth)
    {
        mode = 'long';
        return size;
    }
    // Paysage
    else
    {
        mode = 'large';
        return 0;
    }
}


// Update height
function update_height()
{
    // Update mode
    let size_url = update_mode();

    // Add back class
    let main = document.querySelector('main');
    let nav = document.querySelector('nav').clientHeight;
    if (nav == 45)
    {
        main.setAttribute("style", "height: calc(100vh - 45px)");
    }
    else
    {
        main.setAttribute("style", "height: 92vh");
    }
    

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

    console.log('Height after modification : ' + new_size.toString());
}


// Global var
let prev_mode = 'none';
let mode = 'none';


//Start
document.addEventListener('DOMContentLoaded', function() {
    // Size
    update_height();

    // Rotation
    window.addEventListener('resize', () => {
        update_height();
    });
});