// sleep time expects milliseconds
function sleep(time)
{
    return new Promise((resolve) => setTimeout(resolve, time));
}


async function resize()
{
    await sleep(100);
    // height of content
    let height = window.innerHeight - document.querySelector('nav').offsetHeight;

    if (height > 530)
    {
        let main = document.querySelector('.contact1');
        main.setAttribute('style', 'height: ' + height.toString() + 'px');
    }
}


document.addEventListener('DOMContentLoaded', function() {
    // Update height
    resize();
    
    // resize 
    window.addEventListener('resize', resize);

    // form
    let form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        // vider les champs
        let check = true;
        let inputs = document.querySelectorAll('input');
        let msg = document.querySelector('textarea');

        for (let i = 0 ; i < inputs.length ; i++)
        {
            inputs[i].removeAttribute('style');
            if (! inputs[i].value)
            {
                inputs[i].setAttribute("style", "border: solid 1px red;");
                check = false;
            }
        }

        msg.removeAttribute('style');
        if (! msg.value)
        {
            msg.setAttribute("style", "border: solid 1px red;");
            check = false;
        }

        // formulaire envoyé
        if (check == true)
        {
            for (let i = 0 ; i < inputs.length ; i++)
            {
                inputs[i].value = null;
            }
            msg.value = null;
            alert('Message envoyé !');
        }

        // arreter psq pas de bdd
        event.preventDefault();
    });
});