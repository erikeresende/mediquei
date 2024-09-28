document.addEventListener('DOMContentLoaded', function() {
    var canvas = document.getElementById('signature-pad');
    var signaturePad = new SignaturePad(canvas);

    // Limpar assinatura com efeito de animação
    document.getElementById('clear').addEventListener('click', function () {
        signaturePad.clear();
        alert("Assinatura limpa com sucesso!"); // Feedback do usuário
    });

    // Processar envio do formulário
    document.querySelector('form').addEventListener('submit', function (e) {
        if (!signaturePad.isEmpty()) {
            var dataURL = signaturePad.toDataURL();
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = 'assinatura_digital';
            input.value = dataURL;
            this.appendChild(input);
        } else {
            alert("Por favor, faça uma assinatura antes de enviar."); // Feedback do usuário
            e.preventDefault(); // Previne o envio do formulário se não houver assinatura
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
            <button type="button" class="btn btn-danger btn-sm remove-medicamento">Remover</button>
        `;
        container.appendChild(newItem);

        // Adicionar animação de entrada
        newItem.style.opacity = 0;
        setTimeout(() => {
            newItem.style.opacity = 1; // Anima a entrada do novo item
        }, 50);

        // Adicionar evento de remoção ao novo item
        newItem.querySelector('.remove-medicamento').addEventListener('click', function() {
            newItem.style.transition = 'opacity 0.3s'; // Animação de saída
            newItem.style.opacity = 0;
            setTimeout(() => {
                newItem.remove();
            }, 300); // Remove após a animação
        });
    });

    // Adicionar eventos de remoção aos medicamentos existentes
    document.querySelectorAll('.remove-medicamento').forEach(function(button) {
        button.addEventListener('click', function() {
            var item = this.parentElement;
            item.style.transition = 'opacity 0.3s'; // Animação de saída
            item.style.opacity = 0;
            setTimeout(() => {
                item.remove();
            }, 300); // Remove após a animação
        });
    });
});

document.addEventListener('DOMContentLoaded', () => {
    const content = document.getElementById('content');

    // Quando a página é carregada, adiciona a classe show
    content.classList.add('show');

    // Para transições entre links
    const links = document.querySelectorAll('a');

    links.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault(); // Previne o comportamento padrão do link

            content.classList.remove('show'); // Remove a classe para iniciar a transição de saída

            // Espera o tempo da transição e então redireciona
            setTimeout(() => {
                window.location.href = link.href;
            }, 500); // Tempo da transição em milissegundos
        });
    });
});
