window.addEventListener('DOMContentLoaded', () => {
    const view1Button = document.getElementById('showSecondaryView1');
    const view2Button = document.getElementById('showSecondaryView2');

    view1Button.addEventListener('click', () => {
        window.appapi.showview('mainwiew');    

    });

    view2Button.addEventListener('click', () => {
        window.appapi.showview('settingswiew');   
    
    });

});