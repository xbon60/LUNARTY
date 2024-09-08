const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

/**
 * Fonction pour envoyer un fichier au serveur.
 * @param {string} filePath - Le chemin du fichier à télécharger.
 * @param {string} apiKey - La clé API pour authentifier l'utilisateur.
 * @returns {Promise<object>} - La réponse du serveur.
 */
async function uploadFile(filePath, apiKey) {
  try {
    // Créez un stream de lecture pour le fichier
    const fileStream = fs.createReadStream(filePath);
    
    // Configurez le formulaire de données
    const formData = new FormData();
    formData.append('file', fileStream);

    // Envoyez le fichier au serveur distant avec la clé API
    const response = await axios.post('https://uploadlunarty.cloudnest.ovh/upload', formData, {
      headers: {
        'x-api-key': apiKey,  // Ajoutez la clé API dans les en-têtes
        ...formData.getHeaders() // Ajoutez les headers nécessaires pour le formulaire
      }
    });

    //console.log('Fichier téléchargé avec succès :', response.data);
    return response.data;
  } catch (error) {
    console.error('Erreur lors du téléchargement du fichier :', error);
    throw error;
  }
}

module.exports = uploadFile;
