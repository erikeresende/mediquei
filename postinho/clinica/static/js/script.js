document.addEventListener('DOMContentLoaded', function() {
    var addMedicamentoBtn = document.getElementById('add-medicamento');
    var medicamentosContainer = document.getElementById('medicamentos-container');
    var totalForms = document.getElementById('id_form-TOTAL_FORMS');  // Campo oculto gerado pelo formset
    var currentFormCount = parseInt(totalForms.value);  // Número atual de formulários

    addMedicamentoBtn.addEventListener('click', function() {
        // Clona o primeiro item da lista de medicamentos
        var newForm = medicamentosContainer.children[0].cloneNode(true);

        // Atualiza o índice dos novos campos de medicamento e dosagem
        newForm.querySelectorAll('input').forEach(function(input) {
            var name = input.name.replace(`-${currentFormCount-1}-`, `-${currentFormCount}-`);
            input.name = name;
            input.id = `id_${name}`;
            input.value = '';  // Limpa o valor do campo para o novo medicamento
        });

        medicamentosContainer.appendChild(newForm);
        totalForms.value = currentFormCount + 1;  // Incrementa o contador de forms
        currentFormCount++;
    });
});
