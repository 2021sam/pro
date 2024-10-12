// /Users/2021sam/apps/zyxe/pro/static/js/dynamic_skills_form.js
const formsetBody = document.getElementById('formset-body');
const totalFormsInput = document.querySelector('#id_form-TOTAL_FORMS');  // Django formset management input for total forms

// Function to dynamically add a new form row in the Flexbox structure
function addNewFormRow() {
    let formCount = parseInt(totalFormsInput.value);  // Get the current form count from the management form input
    console.log(`Adding new form row. Current form count: ${formCount}`);

    // Create a new Flexbox row
    const newRow = document.createElement('div');
    newRow.classList.add('form-row');  // Flexbox row

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

    // Append the new Flexbox row to the formset body
    formsetBody.appendChild(newRow);
    console.log('New row added to the formset body.');

    // Increment the total forms count in the management form
    totalFormsInput.value = formCount + 1;
    console.log(`Total forms count updated to: ${totalFormsInput.value}`);
}

// Function to check if the last form row is filled out
function isLastRowFilled() {
    const lastRow = formsetBody.querySelector('.form-row:last-child');
    const skillInput = lastRow.querySelector('input[name$="-skill"]');
    const yearInput = lastRow.querySelector('input[name$="-skill_years"]');
    const monthInput = lastRow.querySelector('input[name$="-skill_months"]');

    // Log the values for debugging
    console.log(`Checking last row: Skill: ${skillInput.value}, Years: ${yearInput.value}, Months: ${monthInput.value}`);

    // Check if the skill is filled and at least one of years or months is non-zero
    return skillInput.value.trim() !== "" && (parseInt(yearInput.value) > 0 || parseInt(monthInput.value) > 0);
}

// Event listener to dynamically add a new row when the last row is filled
document.getElementById('skill-form').addEventListener('input', function () {
    console.log('Input detected.');
    if (isLastRowFilled()) {
        console.log('Last row is filled. Adding new form row.');
        addNewFormRow();  // Add a new empty form row when the last row is filled
    } else {
        console.log('Last row is not filled yet.');
    }
});

// Event listener to handle form submission
document.querySelector('form').addEventListener('submit', function (event) {
    event.preventDefault();  // Prevent form submission to view console logs

    const lastRow = formsetBody.querySelector('.form-row:last-child');
    console.log('Form submission detected.');

    // If the last row is not filled, clear its inputs so it's ignored
    if (!isLastRowFilled()) {
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
