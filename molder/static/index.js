/**
 * Adds interactivity to the website.
 *
 * There are a couple of globals which determine the state.
 *
 * molInchi- The inchi of the molecule currently being viewed.
 *
 * molStructure - The structure of the molecule currently being viewed.
 * The structure is represented using the V3000 .mol format.
 *
 * historyIndex - int - Keeps track of how many molecules the user has
 * viewed.
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
 * Communicates with the server when a button is pressed, excluding ``back``.
 *
 * Tells the server the username, molecule, button pressed and
 * previously seen molecules. Creates a callback for when the server
 * sends back the next molecule to render.
 */
function sendOpinion(username, molecule, opinion) {
    // Don't allow any new requests until this one is complete.
    buttonsOn = false;

    let opinionRequest = new XMLHttpRequest();
    opinionRequest.addEventListener("load", requestListener);

    // Once the opinion is sent, ask the server to send back the
    // new historyIndex.
    let updateHistoryIndexRequest = () => getMaxHistoryIndex(username);
    opinionRequest.addEventListener("load", updateHistoryIndexRequest);

    let url = `/opinions/${username}/${molecule}/${opinion}`;
    opinionRequest.open("POST", url);
    opinionRequest.send();
}


/**
 * A callback function for ``nextMolecule`` and ``getMolecule``.
 *
 * When the server sends back the structure of the next molecule to be
 * rendered, this function is run. It updates ``currentMolecule`` and
 * renders the new molecule.
 */
function updateState() {
    [molInchi, molStructure] = JSON.parse(this.responseText);
    viewer.loadMoleculeStr(undefined, molStructure);
    // Allow new requests to be sent.
    buttonsOn = true;
}


/**
 * Requests the next unseen molecule to render from the server.
 */
function nextMolecule(username)
{
    buttonsOn = false;

    let nextMolRequest = new XMLHttpRequest();
    nextMolRequest.addEventListener("load", requestListener);
    nextMolRequest.addEventListener("load", updateState);
    nextMolRequest.open("GET", `/mols/${username}/next`);
    nextMolRequest.send();
}


/**
 * Communicates with the server when the ``back`` button is pressed.
 *
 * Tells the server the InChI of one of the previous molecules and
 * asks it to return its structure, which is rendered by the callback.
 */
function getHistoricalMolecule(username, historyIndex) {
    // Don't allow any new requests until this one is complete.
    buttonsOn = false;

    let moleculeRequest = new XMLHttpRequest();
    moleculeRequest.addEventListener("load", requestListener);
    moleculeRequest.addEventListener("load", updateState);
    moleculeRequest.open("GET", `/mols/${username}/${historyIndex}`);
    moleculeRequest.send();

}


/**
 * Updates the historyIndex variable.
 *
 * This is a callback for getMaxHistoryIndex.
 */
function updateHistoryIndex() {
    historyIndex = JSON.parse(this.responseText);
}


/**
 * Asks for the maximum history index the user has.
 */
function getMaxHistoryIndex(username) {
    let indexRequest = new XMLHttpRequest();
    initRequest.addEventListener("load", requestListener);
    initRequest.addEventListener("load", updateHistoryIndex);
    initRequest.open("GET", `/history_indices/${username}`);
    initRequest.send();
}

/**
 * Intializes the state when the app is first loaded.
 */
function init()
{
    getMaxHistoryIndex(username);
    nextMolecule(username);
}

/*** End of function declarations. ***/


var viewer;
// Holds the Inchi and 3D structure of the molecule, respectively.
var molInchi = undefined;
var molStructure = undefined;
var historyIndex = undefined;
var buttonsOn = false;
var username = prompt("Username (can be anything)");

$(document).ready(function() {
    viewer = new GLmol("viewer", true);
    init();

    /** Make pressing on the keyboard work. **/

    $(document).keydown(function(key) {
        if (key.which === 49) {

            if (buttonsOn) {
                if (historyIndex === 0) {
                    previousMolecules.splice(0, 0, currentMolecule[0]);
                }
                historyIndex = 0;
                sendOpinion(username, molInchi, 0);
                nextMolecule(username);
            }
        }

        if (key.which === 50) {

            if (buttonsOn) {
                if (historyIndex === 0) {
                    previousMolecules.splice(0, 0, currentMolecule[0]);
                }
                historyIndex = 0;
                sendOpinion(username, molInchi, 1);
                nextMolecule(username);
            }
        }

    });

    /** Make clicking on buttons work. **/

    $("#no").on("click touchstart", function() {
        if (buttonsOn) {
            if (historyIndex === 0) {
                previousMolecules.splice(0, 0, currentMolecule[0]);
            }
            ++historyIndex;
            sendOpinion(username, molInchi, 'not synthesizable');
            nextMolecule(username);
        }
    });

    $("#yes").on("click touchstart", function() {
        if (buttonsOn) {
            if (historyIndex === 0) {
                previousMolecules.splice(0, 0, currentMolecule[0]);
            }
            ++historyIndex;
            sendOpinion(username, molInchi, 'synthesizable');
            nextMolecule(username);
        }
    });

    $("#back").on("click touchstart", function() {
        if (buttonsOn and historyIndex >= 0) {
            getHistoricalMolecule(historyIndex);
            --historyIndex;
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
