export async function verificarStatusWhatsapp() {
    const nomeElem = document.getElementById('whatsappNome');
    const numeroElem = document.getElementById('whatsappNumero');
    const fotoElem = document.getElementById('whatsappFoto');
    const qrImage = document.getElementById('qrImage');
    const qrContainer = document.getElementById('qrContainer');
    const mainContent = document.getElementById('mainContent');
    const connectionMessage = document.getElementById('connectionMessage');
    const logoutSection = document.getElementById('logoutSection');

    try {
        const statusRes = await fetch("http://192.168.99.41:3100/api/sessions/default");
        const statusData = await statusRes.json();

        if (statusData.status === "STOPPED") {
            nomeElem.textContent = "🔄 Sessão parada. Reiniciando...";
            numeroElem.textContent = "";
            fotoElem.src = "";
            qrContainer.style.display = "none";
            
            // Ocultar interface principal e mostrar mensagem de conexão
            mainContent.classList.add('hidden');
            connectionMessage.classList.remove('hidden');
            logoutSection.classList.add('hidden');

            await fetch("http://192.168.99.41:3100/api/sessions/default/start", { method: "POST" });
            return;
        }

        if (statusData.status === "SCAN_QR_CODE") {
            nomeElem.textContent = "📷 Escaneie o QR Code para conectar.";
            numeroElem.textContent = "";
            fotoElem.src = "";
            qrImage.src = "http://192.168.99.41:3100/api/default/auth/qr?format=image";
            qrContainer.style.display = "block";
            
            // Ocultar interface principal e mostrar mensagem de conexão
            mainContent.classList.add('hidden');
            connectionMessage.classList.remove('hidden');
            logoutSection.classList.add('hidden');
            return;
        }

        if (statusData.status === "WORKING" && statusData.engine?.state === "CONNECTED") {
            const profileRes = await fetch("http://192.168.99.41:3100/api/default/profile");
            if (profileRes.ok) {
                const perfil = await profileRes.json();
                nomeElem.textContent = `🟢 ${perfil.name}`;
                numeroElem.textContent = `📞 ${perfil.id?.split("@")[0] || "?"}`;
                fotoElem.src = perfil.picture;
                
                // Mostrar foto do perfil se disponível
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
            
            // Mostrar interface principal e botão de logout, ocultar mensagem de conexão
            mainContent.classList.remove('hidden');
            connectionMessage.classList.add('hidden');
            logoutSection.classList.remove('hidden');
            return;
        }

        nomeElem.textContent = "⚠️ Sessão em estado indefinido.";
        numeroElem.textContent = `Status: ${statusData.status}`;
        fotoElem.src = "";
        fotoElem.style.display = "none";
        fotoElem.parentElement.querySelector('.avatar-placeholder').style.display = "flex";
        qrContainer.style.display = "none";
        
        // Ocultar interface principal e mostrar mensagem de conexão
        mainContent.classList.add('hidden');
        connectionMessage.classList.remove('hidden');
        logoutSection.classList.add('hidden');

    } catch (err) {
        console.error("Erro ao consultar status do WhatsApp:", err);
        nomeElem.textContent = "❌ Erro de conexão com WAHA.";
        numeroElem.textContent = "";
        fotoElem.src = "";
        fotoElem.style.display = "none";
        fotoElem.parentElement.querySelector('.avatar-placeholder').style.display = "flex";
        qrContainer.style.display = "none";
        
        // Ocultar interface principal e mostrar mensagem de conexão
        mainContent.classList.add('hidden');
        connectionMessage.classList.remove('hidden');
        logoutSection.classList.add('hidden');
    }
}

export async function fazerLogoutWhatsapp() {
    const logoutButton = document.getElementById('logoutButton');
    
    try {
        // Desabilitar botão durante o logout
        logoutButton.disabled = true;
        logoutButton.innerHTML = '<span class="logout-icon">⏳</span><span class="logout-text">Desconectando...</span>';
        
        const response = await fetch("http://192.168.99.41:3100/api/sessions/default/logout", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            }
        });
        
        if (response.ok) {
            console.log("Logout realizado com sucesso");
            // Recarregar a página para refletir o novo estado
            window.location.reload();
        } else {
            throw new Error(`Erro no logout: ${response.status}`);
        }
        
    } catch (error) {
        console.error("Erro ao fazer logout:", error);
        
        // Restaurar botão em caso de erro
        logoutButton.disabled = false;
        logoutButton.innerHTML = '<span class="logout-icon">🚪</span><span class="logout-text">Desconectar WhatsApp</span>';
        
        // Mostrar mensagem de erro
        alert("Erro ao desconectar do WhatsApp. Tente novamente.");
    }
}
