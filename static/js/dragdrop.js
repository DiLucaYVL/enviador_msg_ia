export function configurarDragAndDrop() {
    const dropArea = document.querySelector('.file-upload');
    const inputFile = document.getElementById('csvFile');

    if (!dropArea || !inputFile) return;

    // Destaque visual ao arrastar
    ['dragenter', 'dragover'].forEach(event => {
        dropArea.addEventListener(event, e => {
            e.preventDefault();
            e.stopPropagation();
            dropArea.classList.add('drag-over');
        });
    });

    // Remover destaque ao sair
    ['dragleave', 'drop'].forEach(event => {
        dropArea.addEventListener(event, e => {
            e.preventDefault();
            e.stopPropagation();
            dropArea.classList.remove('drag-over');
        });
    });

    // Captura o arquivo e insere no input
    dropArea.addEventListener('drop', e => {
        const file = e.dataTransfer.files[0];
        if (!file) return;

        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        inputFile.files = dataTransfer.files;

        inputFile.dispatchEvent(new Event('change'));
    });
}
