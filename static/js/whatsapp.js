// IMPORTAÇÃO ATUALIZADA
import { carregarConfig } from './config.js';

export async function verificarStatusWhatsapp() {
    const nomeElem = document.getElementById('whatsappNome');
    const numeroElem = document.getElementById('whatsappNumero');
    const fotoElem = document.getElementById('whatsappFoto');
    const qrImage = document.getElementById('qrImage');
    const qrContainer = document.getElementById('qrContainer');
    const mainContent = document.getElementById('mainContent');
    const connectionMessage = document.getElementById('connectionMessage');
    const logoutSection = document.getElementById('logoutSection');

    // 🟢 CARREGANDO CONFIG
    const { api_url } = await carregarConfig();

    try {
        const statusRes = await fetch(`${api_url}/api/sessions/default`);
        const statusData = await statusRes.json();

        const status = statusData.status?.toUpperCase();
        const engineState = statusData.engine?.state?.toUpperCase();

        console.log("📡 Status WAHA:", status);
        console.log("🧠 Engine State:", engineState);

        if (status === "STOPPED") {
            nomeElem.textContent = "🔄 Sessão parada. Reiniciando...";
            numeroElem.textContent = "";
            fotoElem.src = "";
            qrContainer.style.display = "none";

            mainContent.classList.add('hidden');
            connectionMessage.classList.remove('hidden');
            logoutSection.classList.add('hidden');

            await fetch(`${api_url}/api/sessions/default/start`, { method: "POST" });
            return;
        }

        if (status === "STARTING") {
            nomeElem.textContent = "⏳ Inicializando sessão do WhatsApp...";
            numeroElem.textContent = "";
            fotoElem.src = "";
            qrContainer.style.display = "none";

            mainContent.classList.add('hidden');
            connectionMessage.classList.remove('hidden');
            logoutSection.classList.add('hidden');
            return;
        }

        if (status === "SCAN_QR_CODE") {
            nomeElem.textContent = "📷 Escaneie o QR Code para conectar.";
            numeroElem.textContent = "";
            fotoElem.src = "";

            qrImage.src = `${api_url}/api/default/auth/qr?format=image`;
            qrImage.style.display = "block";
            qrContainer.style.display = "block";

            mainContent.classList.add('hidden');
            connectionMessage.classList.remove('hidden');
            logoutSection.classList.add('hidden');

            console.log("🟢 QR Code visível:", qrImage.src);
            return;
        }

        if (status === "WORKING") {
            const profileRes = await fetch(`${api_url}/api/default/profile`);

            if (profileRes.ok) {
                const perfil = await profileRes.json();
                nomeElem.textContent = `🟢 ${perfil.name}`;
                numeroElem.textContent = `📞 ${perfil.id?.split("@")[0] || "?"}`;
                fotoElem.src = perfil.picture;

                if (perfil.picture) {
                    fotoElem.style.display = "block";
                    fotoElem.parentElement.querySelector('.avatar-placeholder').style.display = "none";
                } else {
                    fotoElem.style.display = "none";
                    fotoElem.parentElement.querySelector('.avatar-placeholder').style.display = "flex";
                }
            } else {
                nomeElem.textContent = "🟢 Conectado";
                numeroElem.textContent = "Perfil indisponível";
                fotoElem.src = "";
                fotoElem.style.display = "none";
                fotoElem.parentElement.querySelector('.avatar-placeholder').style.display = "flex";
            }

            qrContainer.style.display = "none";
            mainContent.classList.remove('hidden');
            connectionMessage.classList.add('hidden');
            logoutSection.classList.remove('hidden');
            return;
        }

        if (status === "FAILED") {
            nomeElem.textContent = "❌ Falha ao conectar.";
            numeroElem.textContent = "Tente reiniciar a sessão.";
            fotoElem.src = "";
            fotoElem.style.display = "none";
            fotoElem.parentElement.querySelector('.avatar-placeholder').style.display = "flex";
            qrContainer.style.display = "none";

            mainContent.classList.add('hidden');
            connectionMessage.classList.remove('hidden');
            logoutSection.classList.add('hidden');
            return;
        }

        // Estado desconhecido
        nomeElem.textContent = "⚠️ Sessão em estado indefinido.";
        numeroElem.textContent = `Status: ${statusData.status}`;
        fotoElem.src = "";
        fotoElem.style.display = "none";
        fotoElem.parentElement.querySelector('.avatar-placeholder').style.display = "flex";
        qrContainer.style.display = "none";

        mainContent.classList.add('hidden');
        connectionMessage.classList.remove('hidden');
        logoutSection.classList.add('hidden');

    } catch (err) {
        console.error("❌ Erro ao consultar status do WhatsApp:", err);
        nomeElem.textContent = "❌ Erro de conexão com WAHA.";
        numeroElem.textContent = "";
        fotoElem.src = "";
        fotoElem.style.display = "none";
        fotoElem.parentElement.querySelector('.avatar-placeholder').style.display = "flex";
        qrContainer.style.display = "none";

        mainContent.classList.add('hidden');
        connectionMessage.classList.remove('hidden');
        logoutSection.classList.add('hidden');
    }
}

export async function fazerLogoutWhatsapp() {
    const logoutButton = document.getElementById('logoutButton');

    try {
        const { api_url } = await carregarConfig();

        logoutButton.disabled = true;
        logoutButton.innerHTML = '<span class="logout-icon">⏳</span><span class="logout-text">Desconectando...</span>';

        const response = await fetch(`${api_url}/api/sessions/default/logout`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });

        if (response.ok) {
            console.log("Logout realizado com sucesso");
            window.location.reload();
        } else {
            throw new Error(`Erro no logout: ${response.status}`);
        }

    } catch (error) {
        console.error("Erro ao fazer logout:", error);
        logoutButton.disabled = false;
        logoutButton.innerHTML = '<span class="logout-icon">🚪</span><span class="logout-text">Desconectar WhatsApp</span>';
        alert("Erro ao desconectar do WhatsApp. Tente novamente.");
    }
}
