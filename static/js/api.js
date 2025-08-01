import { mostrarLogs } from './ui.js';

export async function enviarCSV(formData) {
    const botao = document.getElementById('sendButton');
    botao.disabled = true; // 🔒 desativa ao começar
    document.getElementById("sendButton").disabled = true; //desativa o botão de envio

    mostrarLogs([{ type: "info", message: "🚀 Envio iniciado. Processando o arquivo..." }]);

    try {
        const res = await fetch('/enviar', {
            method: 'POST',
            body: formData
        });

        return await res.json();
    } catch (error) {
        mostrarLogs([{ type: "error", message: "❌ Falha na comunicação com o servidor." }]);
        throw error;
    } finally {
        botao.disabled = false; // ✅ reativa ao final (com ou sem erro)
        document.getElementById("sendButton").disabled = false; // reativa o botão de envio
    }
}



export async function obterEquipes(formData) {
    const res = await fetch('/equipes', { method: 'POST', body: formData });
    return await res.json();
}
