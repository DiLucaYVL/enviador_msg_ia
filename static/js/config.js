// static/js/config.js
let CONFIG = null;

export async function carregarConfig() {
    if (CONFIG) return CONFIG;

    try {
        const response = await fetch('/config.json');
        const json = await response.json();

        CONFIG = {
            api_url: json.EVOLUTION_URL,            
            instance: json.EVOLUTION_INSTANCE || "Teste",
            token: json.EVOLUTION_TOKEN || "T0pF4m4D3vs"
        };

        return CONFIG;
    } catch (error) {
        console.error('Erro ao carregar configuração:', error);

        CONFIG = {
            api_url: 'http://192.168.99.41:8080',
            instance: 'Teste',
            token: 'T0pF4m4D3vs'
        };

        return CONFIG;
    }
}

export function getConfig() {
    return CONFIG;
}