/*


*/


function activateButtons() {

}


function deactivateButtons() {

}


/** Prints data returned by a request. */
function requestListener() {
    console.log(this.responseText);
}


function initCallback() {
    [history, currentMolecule] = JSON.parse(this.responseText);
    viewer.loadMoleculeStr(undefined, currentMolecule[1]);
    activateButtons();
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

console.log('hi');

var viewer, history, currentMolecule;
var username = prompt('Username');

$(document).ready(function() {
    viewer = new GLmol('viewer', true);
    init();

});
