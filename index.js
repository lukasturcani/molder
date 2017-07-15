/**
 * Adds interactivity to the website.
 *
 * There are a couple of globals which determine the state.
 *
 * previousMolecules - array of strings - Each string is the InChI of a
 * molecule previously seen by the user. Most recent first.
 *
 * currentMolecule - array of 2 strings - The first string is the
 * InChI of the molecule currently being viewed. The second string is
 * its structure. The structure is represented using the V3000 .mol
 * file format.
 *
 * historyIndex - int - Keeps track of how many times the user pressed
 * ``back`` button in a row. Reset to 0 every time one of the other
 * buttones is pressed.
 *
 * buttonsOn - bool - A switch which prevents buttons from sending
 * multiple requests to the server. Causes the buttons to stop
 * sending requests until a response is received.
 *
 * username - str - The username of the user.
 */


/**
 * Prints data returned by a request.
 *
 * Used as a callback function for requests.
 */
function requestListener() {
    console.log(this.responseText);
}

/**
 * A callback function for ``sendOpinion`` and ``getMolecule``.
 *
 * When the server sends back the structure of the next molecule to be
 * rendered, this function is run. It updates ``currentMolecule`` and
 * renders the new molecule.
 */
function updateState() {
    currentMolecule = JSON.parse(this.responseText);
    viewer.loadMoleculeStr(undefined, currentMolecule[1]);
    // Allow new requests to be sent.
    buttonsOn = true;
}


/**
 * Communicates with the server when a button is pressed, excluding ``back``.
 *
 * Tells the server the username, molecule, button pressed and
 * previously seen molecules. Creates a callback for when the server
 * sends back the next molecule to render.
 */
function sendOpinion(molecule, opinion) {
    // Don't allow any new requests until this one is complete.
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


/**
 * Communicates with the server when the ``back`` button is pressed.
 *
 * Tells the server the InChI of one of the previous molecules and
 * asks it to return its structure, which is rendered by the callback.
 */
function getMolecule(molecule) {
    // Don't allow any new requests until this one is complete.
    buttonsOn = false;

    var formData = new FormData();
    formData.append("molecule", molecule);

    var moleculeRequest = new XMLHttpRequest();
    moleculeRequest.addEventListener("load", requestListener);
    moleculeRequest.addEventListener("load", updateState);
    moleculeRequest.open("POST", "get_mol.cgi");
    moleculeRequest.send(formData);

}


/**
 * A callback for the ``init`` function.
 *
 * When the server returns the molecules previously seen by the user
 * and the molecule which should be rendered, this function saves the
 * data and renders the molecule.
 */
function initCallback() {
    [previousMolecules, currentMolecule] = JSON.parse(this.responseText);
    viewer.loadMoleculeStr(undefined, currentMolecule[1]);
    // Allow requests to be sent to the server.
    buttonsOn = true;
}


/**
 * Asks the server to return any molecules previously seen by the user.
 *
 * Also asks it for the first molecule to be viewed in this session.
 */
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
var historyIndex = 0;
var buttonsOn = false;
var username = prompt("Username");

$(document).ready(function() {
    viewer = new GLmol("viewer", true);
    init();

    $("#no").on("click touchstart", function() {
        if (buttonsOn) {
            if (historyIndex === 0) {
                previousMolecules.splice(0, 0, currentMolecule[0]);
            }
            historyIndex = 0;
            sendOpinion(currentMolecule[0], 0);
        }
    });

    $("#not_sure").on("click touchstart", function() {
        if (buttonsOn) {
            if (historyIndex === 0) {
                previousMolecules.splice(0, 0, currentMolecule[0]);
            }
            historyIndex = 0;
            sendOpinion(currentMolecule[0], 1);
        }
    });

    $("#yes").on("click touchstart", function() {
        if (buttonsOn) {
            if (historyIndex === 0) {
                previousMolecules.splice(0, 0, currentMolecule[0]);
            }
            historyIndex = 0;
            sendOpinion(currentMolecule[0], 2);
        }
    });

    $("#back").on("click touchstart", function() {
        if (buttonsOn && historyIndex < previousMolecules.length) {
            getMolecule(previousMolecules[historyIndex]);
            historyIndex++;
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
