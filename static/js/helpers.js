export function gerarFormData(file, ignorarSabados, debugMode, equipesSelecionadas) {
    const formData = new FormData();
    formData.append('csvFile', file);
    formData.append('ignorarSabados', ignorarSabados);
    formData.append('debugMode', debugMode);
    formData.append('equipesSelecionadas', JSON.stringify(equipesSelecionadas));
    return formData;
}
