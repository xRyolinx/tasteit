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


//Start
document.addEventListener('DOMContentLoaded', function() {
    // Update size and remove cover
    init();

    // Rotation
    window.addEventListener('resize', update_height);
});