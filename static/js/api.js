export async function enviarCSV(formData) {
    const res = await fetch('/enviar', { method: 'POST', body: formData });
    return await res.json();
}

export async function obterEquipes(formData) {
    const res = await fetch('/equipes', { method: 'POST', body: formData });
    return await res.json();
}
