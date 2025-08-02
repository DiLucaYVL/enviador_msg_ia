import { carregarConfig } from './config.js'; // Agora carrega a URL do config.json

document.addEventListener("DOMContentLoaded", function() {
    const avatar = document.querySelector(".avatar-placeholder");
    const modal = document.getElementById("screenshotModal");
    const img = document.getElementById("screenshotImage");
    const refresh = document.getElementById("refreshScreenshot");
    const fechar = document.getElementById("fecharScreenshot");

    if (avatar && modal && img && refresh && fechar) {
        avatar.style.cursor = "pointer";
        avatar.title = "Clique para ver o print da sessão";

        avatar.addEventListener("click", function() {
            modal.style.display = "flex";
        });

        refresh.addEventListener("click", async function() {
            const { api_url } = await carregarConfig(); // Carrega a URL da API do config.json
            img.src = `${api_url}/api/screenshot?session=default&t=` + Date.now();
        });

        fechar.addEventListener("click", function() {
            modal.style.display = "none";
        });
    }
});
