export function carregarDropdownEquipes(equipes) {
    const dropdownList = document.getElementById('dropdownList');
    const selectedCount = document.getElementById('selectedCount');
    const selectAllCheckbox = document.getElementById('selectAllLojas');

    if (!dropdownList || !selectedCount) return;

    dropdownList.innerHTML = '';

    equipes.forEach(equipe => {
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

    // Dropdown toggle
    const dropdownHeader = document.getElementById('dropdownHeader');
    const dropdownContent = document.getElementById('dropdownContent');

    dropdownHeader?.addEventListener('click', () => {
        dropdownHeader.classList.toggle('active');
        dropdownContent.classList.toggle('show');
    });

    document.addEventListener('click', (e) => {
        if (!dropdownHeader.contains(e.target) && !dropdownContent.contains(e.target)) {
            dropdownHeader.classList.remove('active');
            dropdownContent.classList.remove('show');
        }
    });

    // Filtro de busca
    document.getElementById('searchLojas')?.addEventListener('input', function () {
        const termo = this.value.toLowerCase();
        document.querySelectorAll('#dropdownList .dropdown-item').forEach(item => {
            const label = item.querySelector('label').textContent.toLowerCase();
            item.classList.toggle('hidden', !label.includes(termo));
        });
    });
}
