const formsetBody = document.getElementById('formset-body');
const totalFormsInput = document.querySelector('#id_form-TOTAL_FORMS');  // Django formset management input for total forms

// Function to dynamically add a new form row
function addNewFormRow() {
    let formCount = parseInt(totalFormsInput.value);

    const newRow = document.createElement('div');
    newRow.classList.add('form-row');

    newRow.innerHTML = `
        <div class="form-group skill-col">
            <input type="text" name="form-${formCount}-skill" class="textinput textInput form-control" maxlength="100" id="id_form-${formCount}-skill">
        </div>
        <div class="years-months-delete-container">
            <input type="number" name="form-${formCount}-skill_years" class="year-input" min="0" max="10" id="id_form-${formCount}-skill_years">
            <input type="number" name="form-${formCount}-skill_months" class="month-input" min="0" max="11" id="id_form-${formCount}-skill_months">
            <div class="delete-checkbox">
                <input type="checkbox" name="form-${formCount}-DELETE" id="id_form-${formCount}-DELETE">
            </div>
        </div>
    `;

    formsetBody.appendChild(newRow);
    totalFormsInput.value = formCount + 1;
}

// Event listener to dynamically add new row when the last row is filled
document.getElementById('skill-form').addEventListener('input', function () {
    const lastRow = formsetBody.querySelector('.form-row:last-child');
    const skillInput = lastRow.querySelector('input[name$="-skill"]');
    const yearInput = lastRow.querySelector('input[name$="-skill_years"]');
    const monthInput = lastRow.querySelector('input[name$="-skill_months"]');

    if (skillInput.value.trim() !== "" && (parseInt(yearInput.value) > 0 || parseInt(monthInput.value) > 0)) {
        addNewFormRow();
    }
});

// Handle form submission
document.querySelector('form').addEventListener('submit', function () {
    const lastRow = formsetBody.querySelector('.form-row:last-child');
    const skillInput = lastRow.querySelector('input[name$="-skill"]');

    if (!skillInput.value.trim()) {
        formsetBody.removeChild(lastRow); // Remove the last row if it's empty
    }
});
