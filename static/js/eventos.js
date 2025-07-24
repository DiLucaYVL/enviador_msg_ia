import { gerarFormData } from './helpers.js';
import { enviarCSV } from './api.js';
import { mostrarLogs, atualizarEstatisticas, mostrarDebug, atualizarBarraProgresso } from './ui.js';
import { carregarDropdownEquipes } from './dropdown.js';

let arquivoInput = document.getElementById('csvFile');
let arquivoSelecionado = null;  // Arquivo mantido em memória

export function configurarEventos() {
    // Quando o usuário seleciona um arquivo
    arquivoInput.addEventListener('change', async () => {
        arquivoSelecionado = arquivoInput.files[0];  // Armazena o arquivo selecionado
        if (!arquivoSelecionado) return;

        document.getElementById('sendButton').disabled = false;
        document.getElementById('fileName').textContent = `Arquivo selecionado: ${arquivoSelecionado.name}`;
        document.getElementById('fileName').style.display = "block";

        const formData = new FormData();
        formData.append('csvFile', arquivoSelecionado);
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

    // Quando clica no botão Enviar
    document.getElementById('sendButton').addEventListener('click', async () => {
        const fileAtual = arquivoInput.files?.[0] || arquivoSelecionado;

        if (!fileAtual) {
            alert("Selecione um arquivo CSV.");
            return;
        }

        arquivoSelecionado = fileAtual; // Atualiza para manter válido
        const ignorarSabados = document.getElementById('ignorarSabados').checked;
        const debugMode = document.getElementById('debugMode')?.checked || false;

        const equipesSelecionadas = Array.from(document.querySelectorAll('input[name="equipes"]:checked'))
            .map(e => e.value);

        const formData = gerarFormData(fileAtual, ignorarSabados, debugMode, equipesSelecionadas);

        atualizarBarraProgresso("25%");
        console.info("📦 Enviando arquivo:", arquivoSelecionado);

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

            document.getElementById('sendButton').disabled = false;
            document.getElementById('fileName').textContent = `Arquivo mantido: ${arquivoSelecionado.name}`;
            document.getElementById('fileName').style.display = "block";

        } catch (error) {
            console.error("❌ Erro durante envio:", error);
            alert("Erro de rede ou servidor ao enviar mensagens.");
        }
    });
}

