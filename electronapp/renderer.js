document.addEventListener('DOMContentLoaded', () => {
    const displaymoniteur = document.getElementById('displaymoniteur');
    const buttonactivermoniteur = document.getElementById('activermoniteur');
    buttonactivermoniteur.addEventListener('click', () => {
        activer_moniteur(displaymoniteur);
    });
    const buttondesactivermoniteur = document.getElementById('desactivermoniteur');
    buttondesactivermoniteur.addEventListener('click', () => {
        desactiver_moniteur(displaymoniteur);
    });
});

function activer_moniteur(displaymoniteur) {
    let buttonaffichage = "Mode Moniteur ACTIF";
    displaymoniteur.textContent = buttonaffichage;
}

function desactiver_moniteur(displaymoniteur) {
    let buttonaffichage = "Mode Moniteur INACTIF";
    displaymoniteur.textContent = buttonaffichage;
}
