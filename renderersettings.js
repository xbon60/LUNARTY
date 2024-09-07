
window.addEventListener('DOMContentLoaded', () => {
  window.materialapi.configrequest()

  window.refreshapi.configrequest((event, config) => {
        networkcard.value = config.networkcard;
  });


const networkcard = document.getElementById('networkcardvalue');

const saveConfig = document.getElementById('saveConfig');

saveConfig.addEventListener('click', () => {
  window.appapi.logreport('Clic sur le bouton de sauvegarde !');
  const newConfig = {
    networkcard: document.getElementById('networkcardvalue').value,
  };
  window.materialapi.setconfig(newConfig);
});

});




