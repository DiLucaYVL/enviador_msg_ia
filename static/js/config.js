// static/js/config.js
let CONFIG = null;

export async function carregarConfig() {
    if (CONFIG) return CONFIG;
    
    try {
        const response = await fetch('config.json'); // ← agora puxa diretamente do arquivo JSON
        CONFIG = await response.json();
        return CONFIG;
    } catch (error) {
        console.error('Erro ao carregar configuração:', error);
        // Fallback para o IP padrão se não conseguir carregar a configuração
        CONFIG = {
            api_url: 'http://localhost:3000'
        };
        return CONFIG;
    }
}

export function getConfig() {
    return CONFIG;
}
