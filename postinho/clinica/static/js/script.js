document.addEventListener('DOMContentLoaded', function() {
    var canvas = document.getElementById('signature-pad');
    var signaturePad = new SignaturePad(canvas);

    // Limpar assinatura
    document.getElementById('clear').addEventListener('click', function () {
        signaturePad.clear();
    });

    // Processar envio do formulário
    document.querySelector('form').addEventListener('submit', function () {
        if (!signaturePad.isEmpty()) {
            var dataURL = signaturePad.toDataURL();
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'assinatura_digital';
            input.value = dataURL;
            this.appendChild(input);
        }
    });

    // Adicionar novo medicamento
    document.getElementById('add-medicamento').addEventListener('click', function() {
        var container = document.getElementById('medicamentos-container');
        var newItem = document.createElement('div');
        newItem.className = 'medicamento-item mb-3 d-flex align-items-center';
        newItem.innerHTML = `
            <div class="flex-grow-1">
                <input type="text" name="medicamentos[]" class="form-control mb-2" placeholder="Nome do medicamento" />
                <input type="text" name="dosagens[]" class="form-control" placeholder="Dosagem" />
            </div>
            <button type="button" class="btn btn-danger btn-sm remove-medicamento ml-2">Remover</button>
        `;
        container.appendChild(newItem);

        // Adicionar evento de remoção ao novo item
        newItem.querySelector('.remove-medicamento').addEventListener('click', function() {
            newItem.remove();
        });
    });

    // Adicionar eventos de remoção aos medicamentos existentes
    document.querySelectorAll('.remove-medicamento').forEach(function(button) {
        button.addEventListener('click', function() {
            this.parentElement.remove();
        });
    });
});
