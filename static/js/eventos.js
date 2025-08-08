import { gerarFormData } from './helpers.js';
import { enviarCSV } from './api.js';
import { mostrarLogs, atualizarEstatisticas, mostrarDebug, atualizarBarraProgresso } from './ui.js';
import { carregarDropdownEquipes } from './dropdown.js';

let CONFIG = {}; // variável global para guardar o config
let arquivoInput = document.getElementById('csvFile');
let arquivoSelecionado = null;  // Arquivo mantido em memória

export async function carregarConfiguracoes() {
    try {
        const response = await fetch("/static/js/config.json");
        if (!response.ok) throw new Error("Erro ao buscar config.json");
        CONFIG = await response.json();
        console.log("⚙️ Config carregado:", CONFIG);
    } catch (err) {
        console.error("❌ Falha ao carregar config.json:", err);
    }
}

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
        formData.append('tipoRelatorio', document.getElementById('tipoRelatorio').value);

        try {
            const tipoRelatorioAtual = document.getElementById('tipoRelatorio').value;
            const response = await fetch('/equipes', { method: 'POST', body: formData });

            if (!response.ok) {
                const texto = await response.text();  // Evita erro de JSON inválido
                console.warn("Resposta erro (texto):", texto);

                let msgErro = "Erro ao processar o arquivo CSV.";
                if (tipoRelatorioAtual === "Ocorrências") {
                    msgErro = "❌ O tipo de relatório selecionado foi 'Ocorrências', mas o arquivo não contém as colunas esperadas ('Motivo', 'Ação pendente', etc).";
                } else if (tipoRelatorioAtual === "Auditoria") {
                    msgErro = "❌ O tipo de relatório selecionado foi 'Auditoria', mas o arquivo está em formato incorreto.";
                }

                throw new Error(msgErro);
            }

            const data = await response.json();

            if (data.success && Array.isArray(data.equipes)) {
                carregarDropdownEquipes(data.equipes);
            } else {
                alert("Erro desconhecido ao processar o CSV.");
            }

        } catch (err) {
            console.error("Erro ao carregar equipes:", err);
            alert(err.message || "Erro inesperado ao tentar ler o CSV.");
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
        const tipoRelatorio = document.getElementById('tipoRelatorio').value;

        const equipesSelecionadas = Array.from(document.querySelectorAll('input[name="equipes"]:checked'))
            .map(e => e.value);

        const formData = gerarFormData(fileAtual, ignorarSabados, debugMode, equipesSelecionadas, tipoRelatorio);

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

// ✅ Evento global fora das funções
//document.addEventListener("DOMContentLoaded", async () => {
//    await carregarConfiguracoes();  // carrega o config.json
//    configurarEventos();            // ativa os listeners de arquivo e botão
//});
