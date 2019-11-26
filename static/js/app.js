var counter = 1;

function addStep(divName) {
    var addStep = document.createElement('div');
    addStep.setAttribute("class", "input-field col s12 grey lighten-5")
    addStep.innerHTML = "<p>Step " + (counter + 1) + "</p> <div class='input-field col s12 m10'> <i class='material-icons prefix'>linear_scale</i> <textarea name='step" + (counter + 1) + "' id='step' class='materialize-textarea' required> </textarea> <label for='step'>Steps to make project</label></div><button type='button' class='remove btn tooltipped waves-effect waves-light red accent-4 valign-wrapper' onclick='removeStep()' data-position='top' data-tooltip='This cannot tbe undone'><i class='material-icons'>delete</i></button>";
    document.getElementById(divName).appendChild(addStep);
    counter++;
}

function removeStep() {
    var btn = document.getElementsByClassName('remove')
    for (var i = 0; i < btn.length; i++) {
        btn[i].addEventListener('click', function (e) {
            e.currentTarget.parentNode.remove();
             M.toast({html: 'Step Removed', classes: 'green darken-2'})
            //this.closest('.single').remove() // in modern browsers in complex dom structure
            //this.parentNode.remove(); //this refers to the current target element 
            //e.target.parentNode.parentNode.removeChild(e.target.parentNode);
        }, false);
    }
}