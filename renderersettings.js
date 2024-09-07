
window.addEventListener('DOMContentLoaded', () => {
  window.materialapi.configrequest()

  window.refreshapi.configrequest((event, config) => {
        console.log('Carte Réseau:', config.networkcard);
        networkcard.value = config.networkcard;
  });


const networkcard = document.getElementById('networkcardvalue');

const saveConfig = document.getElementById('saveConfig');

saveConfig.addEventListener('click', () => {
  console.log('Clic sur le bouton de sauvegarde !');
  const newConfig = {
    networkcard: document.getElementById('networkcardvalue').value,
  };
  window.materialapi.setconfig(newConfig);
});

});




