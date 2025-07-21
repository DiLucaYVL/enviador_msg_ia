let arquivoSelecionado = null;

document.getElementById('sendButton').addEventListener('click', async () => {
    const file = arquivoSelecionado;
    const ignorarSabados = document.getElementById('ignorarSabados').checked;
    const debugMode = document.getElementById('debugMode')?.checked || false;

    if (!file) {
        alert("Selecione um arquivo CSV primeiro.");
        return;
    }

    const formData = new FormData();
    formData.append('csvFile', file);
    formData.append('ignorarSabados', ignorarSabados);
    formData.append('debugMode', debugMode);

    const equipesSelecionadas = Array.from(document.querySelectorAll('input[name="equipes"]:checked'))
        .map(e => e.value);
    formData.append('equipesSelecionadas', JSON.stringify(equipesSelecionadas));

    const logContainer = document.getElementById('logContainer');
    const progressFill = document.getElementById('progressFill');
    logContainer.innerHTML = `<div class="log-entry log-info">⏳ Enviando mensagens...</div>`;
    progressFill.style.width = "25%";

    const response = await fetch('/enviar', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    logContainer.innerHTML = "";

    if (data.success) {
        data.log.forEach(entry => {
            const div = document.createElement('div');
            div.classList.add('log-entry', `log-${entry.type}`);
            div.textContent = entry.message;
            logContainer.appendChild(div);
        });

        document.getElementById('totalMessages').textContent = data.stats.total;
        document.getElementById('totalTeams').textContent = data.stats.equipes;
        document.getElementById('successCount').textContent = data.stats.sucesso;
        document.getElementById('errorCount').textContent = data.stats.erro;
        progressFill.style.width = "100%";

        if (debugMode && data.debug) {
            const debugPanel = document.getElementById('debugPanel');
            const debugContent = document.getElementById('debugContent');
            debugContent.textContent = JSON.stringify(JSON.parse(data.debug), null, 2);
            debugPanel.style.display = "block";
        }
    } else {
        const div = document.createElement('div');
        div.classList.add('log-entry', `log-error`);
        div.textContent = data.log?.[0] || "Erro desconhecido.";
        logContainer.appendChild(div);
        progressFill.style.width = "0%";
        alert(data.log?.[0] || "Erro desconhecido.");
    }
});

document.getElementById('csvFile').addEventListener('change', async () => {
    const file = document.getElementById('csvFile').files[0];
    if (!file) return;

    arquivoSelecionado = file;

    document.getElementById('sendButton').disabled = false;
    const fileNameDiv = document.getElementById('fileName');
    fileNameDiv.textContent = `Arquivo selecionado: ${file.name}`;
    fileNameDiv.style.display = "block";

    const formData = new FormData();
    formData.append('csvFile', file);
    formData.append('ignorarSabados', document.getElementById('ignorarSabados').checked);

    const response = await fetch('/equipes', {
        method: 'POST',
        body: formData
    });

    const data = await response.json();
    if (data.success && Array.isArray(data.equipes)) {
        const dropdownList = document.getElementById('dropdownList');
        const selectedCount = document.getElementById('selectedCount');
        const selectAllCheckbox = document.getElementById('selectAllLojas');

        dropdownList.innerHTML = '';

        data.equipes.forEach(equipe => {
            const dropdownItem = document.createElement('div');
            dropdownItem.className = 'dropdown-item';
            dropdownItem.innerHTML = `
                <input type="checkbox" name="equipes" value="${equipe}" checked />
                <label>${equipe}</label>
            `;
            dropdownList.appendChild(dropdownItem);
        });

        function atualizarContadorSelecionadas() {
            const checkboxes = document.querySelectorAll('#dropdownList input[type="checkbox"]');
            const total = checkboxes.length;
            const selecionadas = Array.from(checkboxes).filter(cb => cb.checked).length;
            if (selecionadas === total) {
                selectedCount.textContent = `Todas as lojas (${total})`;
            } else if (selecionadas === 0) {
                selectedCount.textContent = 'Nenhuma loja selecionada';
            } else {
                selectedCount.textContent = `${selecionadas} de ${total} lojas`;
            }
        }

        dropdownList.querySelectorAll('input[type="checkbox"]').forEach(cb => {
            cb.addEventListener('change', atualizarContadorSelecionadas);
        });

        if (selectAllCheckbox) {
            selectAllCheckbox.addEventListener('change', () => {
                const checkboxes = dropdownList.querySelectorAll('input[type="checkbox"]');
                checkboxes.forEach(cb => cb.checked = selectAllCheckbox.checked);
                atualizarContadorSelecionadas();
            });
        }

        atualizarContadorSelecionadas();
    }

    // Dropdown toggle
    const dropdownHeader = document.getElementById('dropdownHeader');
    const dropdownContent = document.getElementById('dropdownContent');

    dropdownHeader.addEventListener('click', () => {
        dropdownHeader.classList.toggle('active');
        dropdownContent.classList.toggle('show');
    });

    document.addEventListener('click', (e) => {
        if (!dropdownHeader.contains(e.target) && !dropdownContent.contains(e.target)) {
            dropdownHeader.classList.remove('active');
            dropdownContent.classList.remove('show');
        }
    });
});
