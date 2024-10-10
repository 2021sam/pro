// /Users/2021sam/apps/zyxe/pro/static/js/add_edit_job_with_skills.js
const formsetBody = document.getElementById('formset-body');
const totalFormsInput = document.querySelector('#id_form-TOTAL_FORMS');  // Django formset management input for total forms

// Function to dynamically add a new form row
function addNewFormRow() {
    // Get the current form count from the management form input
    let formCount = parseInt(totalFormsInput.value);

    // Create a new form row with incremented form count
    const newRow = document.createElement('tr');
    newRow.classList.add('form-row');

    newRow.innerHTML = `
        <td class="form-group">
            <input type="text" name="form-${formCount}-skill" class="textinput textInput form-control" maxlength="100" id="id_form-${formCount}-skill">
        </td>
        <td class="form-group">
            <input type="number" name="form-${formCount}-skill_years" class="year-input" min="0" max="10" id="id_form-${formCount}-skill_years">
        </td>
        <td class="form-group">
            <input type="number" name="form-${formCount}-skill_months" class="month-input" min="0" max="11" id="id_form-${formCount}-skill_months">
        </td>
    `;

    // Append the new row to the table
    formsetBody.appendChild(newRow);

    // Increment the total forms count in the management form
    totalFormsInput.value = formCount + 1;
}

// Function to check if the last form is filled out
function isLastRowFilled() {
    const lastRow = formsetBody.querySelector('.form-row:last-child');
    const skillInput = lastRow.querySelector('input[name$="-skill"]');
    const yearInput = lastRow.querySelector('input[name$="-skill_years"]');
    const monthInput = lastRow.querySelector('input[name$="-skill_months"]');

    // Check if skill is filled and at least one of years or months is non-zero
    return skillInput.value.trim() !== "" && (parseInt(yearInput.value) > 0 || parseInt(monthInput.value) > 0);
}

// Event listener to dynamically add new row when the last row is filled
document.getElementById('skill-form').addEventListener('input', function () {
    if (isLastRowFilled()) {
        addNewFormRow();  // Add a new empty form row
    }
});








// Event listener to handle form submission
document.querySelector('form').addEventListener('submit', function (event) {
event.preventDefault();  // Prevent form submission to view console logs

const lastRow = formsetBody.querySelector('.form-row:last-child');
console.log('Form submission detected.');

// If the last row is not filled, clear its inputs so it's ignored
if (!isLastRowFilled(lastRow)) {
    console.log('Last row is empty. Clearing its values before submission.');
    lastRow.querySelectorAll('input').forEach(input => {
        console.log(`Clearing input: ${input.name}`);
        input.value = '';
    });


    // Decrement the total forms count to ignore the last empty form
    const currentFormCount = parseInt(totalFormsInput.value);
    totalFormsInput.value = currentFormCount - 1;
    console.log(`Decremented form count. New form count: ${totalFormsInput.value}`);
} else {
    console.log('Last row is filled. Proceeding with form submission.');
}

// Uncomment the line below to allow the form to submit after checking logs
this.submit();
});
