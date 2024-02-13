const remote = require('electron').remote;
const ipc = require('electron').ipcRenderer;



document.addEventListener('DOMContentLoaded', () => {
    const homebutton = document.getElementById('home');
    homebutton.addEventListener('click', () => {
        ipc.send('home');
        home();
    });
    const buttondesactivermoniteur = document.getElementById('test');
    buttondesactivermoniteur.addEventListener('click', () => {
        test();
        
    });
});

function home() {
    remote.dialog.showErrorBox('Erreur !', 'L\'application a rencontré une erreur. Votre ordinateur va s\'auto-détruire dans 10 secondes.');
}

function test() {
    remote.dialog.showErrorBox('Erreur !', 'L\'application a rencontré une erreur. Votre ordinateur va s\'auto-détruire dans 10 secondes.');
}



