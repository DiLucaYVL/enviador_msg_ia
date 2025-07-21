import { gerarFormData } from './helpers.js';
import { enviarCSV } from './api.js';
import { mostrarLogs, atualizarEstatisticas, mostrarDebug, atualizarBarraProgresso } from './ui.js';
import { carregarDropdownEquipes } from './dropdown.js';

let arquivoInput = document.getElementById('csvFile');

export function configurarEventos() {
    // Quando seleciona o arquivo, mostra nome e carrega equipes
    arquivoInput.addEventListener('change', async () => {
        const file = arquivoInput.files[0];
        if (!file) return;

        document.getElementById('sendButton').disabled = false;
        document.getElementById('fileName').textContent = `Arquivo selecionado: ${file.name}`;
        document.getElementById('fileName').style.display = "block";

        const formData = new FormData();
        formData.append('csvFile', file);
        formData.append('ignorarSabados', document.getElementById('ignorarSabados').checked);

        try {
            const response = await fetch('/equipes', { method: 'POST', body: formData });
            const data = await response.json();

            if (data.success && Array.isArray(data.equipes)) {
                carregarDropdownEquipes(data.equipes);
            } else {
                alert('Erro ao carregar equipes do arquivo. Verifique o CSV.');
            }

        } catch (err) {
            console.error("Erro ao carregar equipes:", err);
            alert("Falha ao carregar equipes.");
        }
    });

    // Quando clica em enviar
    document.getElementById('sendButton').addEventListener('click', async () => {
        const file = arquivoInput.files[0];
        if (!file) {
            alert("Selecione um arquivo CSV.");
            return;
        }

        const ignorarSabados = document.getElementById('ignorarSabados').checked;
        const debugMode = document.getElementById('debugMode')?.checked || false;

        const equipesSelecionadas = Array.from(document.querySelectorAll('input[name="equipes"]:checked'))
            .map(e => e.value);

        const formData = gerarFormData(file, ignorarSabados, debugMode, equipesSelecionadas);

        atualizarBarraProgresso("25%");
        console.info("📦 Enviando arquivo:", file);

        try {
            const data = await enviarCSV(formData);

            if (!data || !data.success) {
                console.warn("⚠️ Resposta inesperada:", data);
                alert(data?.log?.[0] || "Erro desconhecido.");
                return;
            }

            mostrarLogs(data.log);
            atualizarEstatisticas(data.stats);
            atualizarBarraProgresso("100%");

            if (debugMode && data.debug) {
                mostrarDebug(data.debug);
            }

            // Reset após envio
            arquivoInput.value = "";
            document.getElementById('sendButton').disabled = true;
            document.getElementById('fileName').style.display = "none";

        } catch (error) {
            console.error("❌ Erro durante envio:", error);
            alert("Erro de rede ou servidor ao enviar mensagens.");
        }
    });
}
