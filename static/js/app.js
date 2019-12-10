// ? Masonary Gird initialize. Displays a loader on the page until all images are loaded and ready
// ? to display the projects in the correct format.

var $grid = $('.grid')

$grid.hide()

$grid.imagesLoaded(function () {
    // Hide loader once images in grid have loaded
    $('.loader').hide()
    $grid.show()
    // init Masonry after all images have loaded
    $grid.masonry({
        itemSelector: '.grid-item',
        columnWidth: '.grid-sizer',
        percentPosition: true
    });

});

// ? FUnctions to add and remove new step and material input fields on the add and edit project pages.

var step_counter = 1;
var material_counter = 1;

// ? Adds a new step input to the add project or edit project page.
function addStep(divName) {
    var addStep = document.createElement('div');
    addStep.setAttribute("class", "input-field col s12")
    addStep.innerHTML = "<p>Step " + (step_counter + 1) + "</p> <div class='input-field col s12 m10'> <i class='material-icons prefix'>linear_scale</i> <textarea name='step'id='step" + (step_counter + 1) + "' class='materialize-textarea'> </textarea> <label for='step" + (step_counter + 1) + "'>Steps to make project</label></div><button type='button' class='remove btn-small tooltipped waves-effect waves-light red accent-4 valign-wrapper' onclick='removeStep()'><i class='material-icons '>delete</i></button>";
    document.getElementById(divName).appendChild(addStep);
    step_counter++;
}

// ? Remvoes a step input from the add project or edit project page.
function removeStep() {
    var btn = document.getElementsByClassName('remove')
    for (var i = 0; i < btn.length; i++) {
        btn[i].addEventListener('click', function (e) {
            e.currentTarget.parentNode.remove();
            M.toast({
                html: 'Step Removed',
                classes: 'green darken-2'
            })
            //this.closest('.single').remove() // in modern browsers in complex dom structure
            //this.parentNode.remove(); //this refers to the current target element 
            //e.target.parentNode.parentNode.removeChild(e.target.parentNode);
        }, false);
    }
}

// ? Adds a new material input to the add project or edit project page.
function addMaterial(divName) {
    var addMaterial = document.createElement('div');
    addMaterial.setAttribute("class", "input-field col s12")
    addMaterial.innerHTML = "<p>Material " + (material_counter + 1) + "</p> <div class='input-field col s12 m10'> <i class='material-icons prefix'>linear_scale</i> <input name='material' id='material" + (material_counter + 1) + "' type='text' class='validate'><label for='material" + (material_counter + 1) + "'>Materials to make project</label></div><button type='button' class='removeMaterial btn tooltipped waves-effect waves-light red accent-4 valign-wrapper' onclick='removeMaterial()'><i class='material-icons'>delete</i></button>";
    document.getElementById(divName).appendChild(addMaterial);
    material_counter++;
}

// ? Removes a material input from the add project or edit project page.
function removeMaterial() {
    var btn = document.getElementsByClassName('removeMaterial')
    for (var i = 0; i < btn.length; i++) {
        btn[i].addEventListener('click', function (e) {
            e.currentTarget.parentNode.remove();
            M.toast({
                html: 'Material Removed',
                classes: 'green darken-2'
            })
            material_counter--;
            //this.closest('.single').remove() // in modern browsers in complex dom structure
            //this.parentNode.remove(); //this refers to the current target element 
            //e.target.parentNode.parentNode.removeChild(e.target.parentNode);
        }, false);
    }
}