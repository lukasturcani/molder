/*


*/


/** Prints data returned by a request. */
function requestListener() {
    console.log(this.responseText);
}


function updateState() {
    currentMolecule = JSON.parse(this.responseText);
    viewer.loadMoleculeStr(undefined, currentMolecule[1]);
    buttonsOn = true;
}


function sendOpinion(molecule, opinion) {
    buttonsOn = false;

    var formData = new FormData();
    formData.append("username", username);
    formData.append("molecule", molecule);
    formData.append("opinion", opinion);
    formData.append("history", JSON.stringify(previousMolecules));

    var opinionRequest = new XMLHttpRequest();
    opinionRequest.addEventListener("load", requestListener);
    opinionRequest.addEventListener("load", updateState);
    opinionRequest.open("POST", "next_mol.cgi");
    opinionRequest.send(formData);
}



function initCallback() {
    [previousMolecules, currentMolecule] = JSON.parse(this.responseText);
    viewer.loadMoleculeStr(undefined, currentMolecule[1]);
    buttonsOn = true;
}


function init() {
    var formData = new FormData();
    formData.append("username", username);

    var initRequest = new XMLHttpRequest();
    initRequest.addEventListener("load", requestListener);
    initRequest.addEventListener("load", initCallback);
    initRequest.open("POST", "init_state.cgi");
    initRequest.send(formData);
}


/*** End of function declarations. ***/


var viewer, previousMolecules, currentMolecule;
var buttonsOn = false;
var username = prompt("Username");

$(document).ready(function() {
    viewer = new GLmol("viewer", true);
    init();

    $("#no").on("click touchstart", function() {
        if (buttonsOn) {
            previousMolecules.splice(0, 0, currentMolecule[0]);
            sendOpinion(currentMolecule[0], 0);
        }
    });

    $("#not_sure").on("click touchstart", function() {
        if (buttonsOn) {
            previousMolecules.splice(0, 0, currentMolecule[0]);
            sendOpinion(currentMolecule[0], 1);
        }
    });

    $("#yes").on("click touchstart", function() {
        if (buttonsOn) {
            previousMolecules.splice(0, 0, currentMolecule[0]);
            sendOpinion(currentMolecule[0], 2);
        }
    });

    /** Make buttons change colour on mouseover. */
    $(".button").hover(
        function(){
            $(this).fadeTo("fast", 0.5);
        },
        function() {
            $(this).fadeTo("fast", 1);
        }
    );

});
