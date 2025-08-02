// static/js/main.js
import { configurarEventos } from './eventos.js';
import { verificarStatusWhatsapp, fazerLogoutWhatsapp } from './whatsapp.js';
import { configurarDragAndDrop } from './dragdrop.js';
import { carregarConfig } from './config.js'; //config para o link do waha

window.addEventListener('DOMContentLoaded', async () => {
    await carregarConfig(); // carrega a config do waha
    
    configurarEventos();
    configurarDragAndDrop();
    verificarStatusWhatsapp();
    setInterval(verificarStatusWhatsapp, 5000);
    
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', fazerLogoutWhatsapp);
    }
});