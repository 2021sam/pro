// /Users/2021sam/apps/zyxe/pro/static/js/formset.js
// /Users/2021sam/apps/zyxe/pro/static/js/formset.js

let debounceTimer;
const maxForms = 10;  // Set a maximum number of rows

function debounce(callback, delay) {
    return function(...args) {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => callback.apply(this, args), delay);
    };
}

// Print the details of each form row to the console
function printFormRows() {
    const formRows = document.querySelectorAll('.form-row');
    console.log(`Printing ${formRows.length} form rows:`);
    formRows.forEach((formRow, index) => {
        const formId = formRow.id || `Form Row ${index + 1}`;  // Use the row's ID or default to a numbered label
        const skillInput = formRow.querySelector('[name$="-skill"]');
        const formName = skillInput.name;  // Get the form name from the skill input
        const skill = skillInput.value;
        const skillYears = formRow.querySelector('[name$="-skill_years"]').value;
        const skillMonths = formRow.querySelector('[name$="-skill_months"]').value;
        console.log(`Row ${index + 1} (ID: ${formId}, Name: ${formName}): Skill: ${skill}, Skill Years: ${skillYears}, Skill Months: ${skillMonths}`);
    });
}

// Validate a single form row
function validateRow(formRow) {
    // Check if formRow is a single element and log it
    if (!(formRow instanceof HTMLElement) || !formRow.classList.contains('form-row')) {
        console.error('Invalid formRow passed to validateRow:', formRow);
        return false; // Return false if the form row is invalid
    }

    console.log('Validating form row:', formRow.id || formRow);

    let isValid = true;

    // Clear existing error messages
    formRow.querySelectorAll('.error-message').forEach(msg => msg.remove());

    // Validate skill input
    const skillInput = formRow.querySelector('[name$="-skill"]');
    if (skillInput.value.trim() === '') {
        isValid = false; // Mark the row as invalid if the skill input is empty
        const error = document.createElement('div');
        error.className = 'error-message';
        error.textContent = 'This field is required.';
        skillInput.parentElement.appendChild(error);
    }

    // Validate skill years and months
    const skillYearsInput = formRow.querySelector('[name$="-skill_years"]');
    const skillMonthsInput = formRow.querySelector('[name$="-skill_months"]');
    if (skillYearsInput.value.trim() === '' && skillMonthsInput.value.trim() === '') {
        isValid = false; // Mark the row as invalid if both fields are empty
        const error = document.createElement('div');
        error.className = 'error-message';
        error.textContent = 'Either skill years or skill months must be filled.';
        skillYearsInput.parentElement.appendChild(error);
    }

    // Apply validation styles
    if (isValid) {
        formRow.classList.remove('invalid-row');
    } else {
        formRow.classList.add('invalid-row');
    }

    return isValid; // Return the validity status of the row
}

// Handle input events for form fields
function handleInputEvent(event) {
    const formRow = event.target.closest('.form-row');
    const formRows = Array.from(document.querySelectorAll('.form-row'));
    const rowIndex = formRows.indexOf(formRow);
    const isLastRow = rowIndex === formRows.length - 1; // Check if the current row is the last one
    const isOnlyRow = formRows.length === 1; // Check if it's the only row

    console.log('Input event on row:', formRow, 'Is last row:', isLastRow, 'Row index:', rowIndex, 'Total rows:', formRows.length);

    // Validate the row if it's not the last row or if it's the only row
    if (!isLastRow || isOnlyRow) {
        console.log('Validating row:', formRow);
        validateRow(formRow);
    } else {
        console.log('Skipping validation for the last row:', formRow);
    }

    // Handle adding new forms
    if (event.target.name.includes('skill')) {
        // Only add a new form if the skill input is not empty
        const lastSkillInput = formRow.querySelector('[name$="-skill"]');
        if (lastSkillInput.value.trim() !== '') {
            console.log('Skill field changed, adding new form.');
            addNewForm();
        }
    }

    // Check for skill years or months input
    if (event.target.name.includes('skill_years') || event.target.name.includes('skill_months')) {
        const skillInput = formRow.querySelector('[name$="-skill"]');
        const skillYears = formRow.querySelector('[name$="-skill_years"]').value.trim();
        const skillMonths = formRow.querySelector('[name$="-skill_months"]').value.trim();

        // Add a new form if both skill input and at least one of years/months is filled
        if (skillInput.value.trim() !== '' && (skillYears !== '' || skillMonths !== '')) {
            console.log('Year or month data entered, adding new form.');
            addNewForm();
        }
    }
}

// Function to add a new form row
function addNewForm() {
    const formRows = document.querySelectorAll('.form-row');
    const lastForm = formRows[formRows.length - 1];
    const lastSkillInput = lastForm.querySelector('[name$="-skill"]');

    if (formRows.length >= maxForms) {
        return;  // Stop adding new rows if the maximum is reached
    }

    // Clone the last form and reset its values
    if (lastSkillInput.value.trim() !== '') {
        const newRow = lastForm.cloneNode(true);
        newRow.querySelectorAll('input').forEach(input => input.value = '');

        const newFormIndex = formRows.length;
        newRow.querySelectorAll('input, select').forEach(input => {
            const name = input.getAttribute('name');
            if (name) {
                const newName = name.replace(/\d+/, newFormIndex);
                input.setAttribute('name', newName);
                input.setAttribute('id', `id_${newName}`);
            }
        });

        document.getElementById('formset-container').appendChild(newRow);
        updateManagementFormCount(); // Update the total form count

        // Attach event listeners to inputs in the new row only
        newRow.querySelectorAll('[name$="-skill"], [name$="-skill_years"], [name$="-skill_months"]').forEach(input => {
            input.addEventListener('input', debounce(handleInputEvent, 500));
        });

        printFormRows(); // Print the current form rows for debugging
    }
}

// Update the total forms count in the management form
function updateManagementFormCount() {
    const formsetContainer = document.getElementById('formset-container');
    const totalForms = formsetContainer.querySelectorAll('.form-row').length;
    const managementForm = formsetContainer.querySelector('input[name$="-TOTAL_FORMS"]');
    if (managementForm) {
        managementForm.value = totalForms; // Set the total forms count
    }
}

// Remove any empty forms before submission
function removeEmptyForms() {
    const formRows = document.querySelectorAll('.form-row');
    formRows.forEach((formRow, index) => {
        const skillInput = formRow.querySelector('[name$="-skill"]');
        if (!skillInput.value.trim()) {
            console.log(`Removing empty form row: ${index}`);
            formRow.remove(); // Remove the empty row
        }
    });
}

// Function to check if a form row is empty
function isFormEmpty(formRow) {
    const skillInput = formRow.querySelector('[name$="-skill"]');
    return skillInput && skillInput.value.trim() === ''; // Return true if the form row is empty
}

// Attach submit event listener to the form
document.querySelector('form').addEventListener('submit', function(event) {
    console.log('Form submission triggered.');
    removeEmptyForms(); // Remove any empty form rows
    updateManagementFormCount(); // Update the total forms count
    printFormRows();  // Print the form rows before submission

    // Run validation on all rows before submission
    const formRows = document.querySelectorAll('.form-row');
    let allValid = true; // Flag to check if all form rows are valid
    formRows.forEach(formRow => {
        if (!validateRow(formRow)) {
            allValid = false; // Set flag to false if any row is invalid
        }
    });

    // Prevent submission if any row is invalid
    if (!allValid) {
        console.log('Form contains validation errors. Submission prevented.');
        event.preventDefault(); // Prevent the form from submitting if validation fails
    }
});

// Attach event listeners to existing skill, skill_years, and skill_months inputs once on initial load
document.querySelectorAll('[name$="-skill"], [name$="-skill_years"], [name$="-skill_months"]').forEach(input => {
    input.addEventListener('input', debounce(handleInputEvent, 500));  // Adjust the delay as needed
});
