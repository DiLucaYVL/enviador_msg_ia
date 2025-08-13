// static/js/config.js
let CONFIG = null;

export async function carregarConfig() {
    if (CONFIG) return CONFIG;

            const response = await fetch('/static/config.json', { cache: 'no-store' });
        const json = await response.json();

        CONFIG = {
            api_url: json.EVOLUTION_URL,            
            instance: json.EVOLUTION_INSTANCE,
            token: json.EVOLUTION_TOKEN
        };

        return CONFIG;
}

export function getConfig() {
    return CONFIG;
}