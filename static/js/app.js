var counter = 1;

function addStep(divName) {

    var addStep = document.createElement('div');
    addStep.setAttribute("class", "input-field col s12")


    addStep.innerHTML = "Step " + (counter + 1) + " <br> <div class='input-field col s12'> <i class='material-icons prefix'>linear_scale</i> <textarea name='stepInput[" + (counter + 1) + "]' id='steps' class='materialize-textarea' required> </textarea> <label for='steps'>Steps to make project</label></div>";

    document.getElementById(divName).appendChild(addStep);

    counter++;
}