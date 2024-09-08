
window.addEventListener('DOMContentLoaded', () => {
  const view1Button = document.getElementById('showmainmenu');
  const view2Button = document.getElementById('showsettingsmenu');
  window.materialapi.configrequest()

  window.refreshapi.configrequest((event, config) => {
        networkcard.value = config.networkcard;
        apivalue.value = config.apiKey;
  });


  view1Button.addEventListener('click', () => {
    window.appapi.showview('mainwiew');    

  });

  view2Button.addEventListener('click', () => {
      window.appapi.showview('settingswiew');   

  });


const networkcard = document.getElementById('networkcardvalue');
const apivalue = document.getElementById('apikeyvalue');

const saveConfig = document.getElementById('saveConfig');

saveConfig.addEventListener('click', () => {
  window.appapi.logreport('Clic sur le bouton de sauvegarde !');
  const newConfig = {
    networkcard: document.getElementById('networkcardvalue').value,
  };
  window.materialapi.setconfig(newConfig);
});

});




