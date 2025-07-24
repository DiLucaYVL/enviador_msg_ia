import { configurarEventos } from './eventos.js';
import { verificarStatusWhatsapp, fazerLogoutWhatsapp } from './whatsapp.js';
import { configurarDragAndDrop } from './dragdrop.js'; 

window.addEventListener('DOMContentLoaded', () => {
    configurarEventos();                            // Inicializa os eventos do app (upload, envio, etc.)
    configurarDragAndDrop();                        // 🟢 Ativa o suporte a arrastar e soltar
    verificarStatusWhatsapp();                      // Checa o status do WhatsApp ao carregar
    setInterval(verificarStatusWhatsapp, 5000);     // Atualiza status a cada 5s
    
    // Configurar evento de logout
    const logoutButton = document.getElementById('logoutButton');
    if (logoutButton) {
        logoutButton.addEventListener('click', fazerLogoutWhatsapp);
    }
});
