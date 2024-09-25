// /Users/2021sam/apps/zyxe/pro/static/js/formset.js
let debounceTimer;
const maxForms = 10;  // Set a maximum number of rows

function debounce(callback, delay) {
    return function(...args) {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => callback.apply(this, args), delay);
    };
}

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
        const experience = formRow.querySelector('[name$="-experience"]').value;
        console.log(`Row ${index + 1} (ID: ${formId}, Name: ${formName}): Skill: ${skill}, Skill Years: ${skillYears}, Skill Months: ${skillMonths}, Experience: ${experience}`);
    });
}

function validateRow(formRow) {
    // Check if formRow is a single element and log it
    if (!(formRow instanceof HTMLElement) || !formRow.classList.contains('form-row')) {
        console.error('Invalid formRow passed to validateRow:', formRow);
        return false;
    }

    // Log the form row ID or a distinguishing feature
    console.log('Validating form row:', formRow.id || formRow);

    let isValid = true;

    // Clear existing error messages
    formRow.querySelectorAll('.error-message').forEach(msg => msg.remove());

    // Validate skill input
    const skillInput = formRow.querySelector('[name$="-skill"]');
    if (skillInput.value.trim() === '') {
        isValid = false;
        const error = document.createElement('div');
        error.className = 'error-message';
        error.textContent = 'This field is required.';
        skillInput.parentElement.appendChild(error);
    }

    // Validate skill years and months
    const skillYearsInput = formRow.querySelector('[name$="-skill_years"]');
    const skillMonthsInput = formRow.querySelector('[name$="-skill_months"]');
    if (skillYearsInput.value.trim() === '' && skillMonthsInput.value.trim() === '') {
        isValid = false;
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

    return isValid;
}

function handleInputEvent(event) {
    const formRow = event.target.closest('.form-row');
    const formRows = Array.from(document.querySelectorAll('.form-row'));
    const rowIndex = formRows.indexOf(formRow);
    const isLastRow = rowIndex === formRows.length - 0; // Check if the current row is the last one
    const isOnlyRow = formRows.length === 1; // Check if it's the only row

    console.log('Input event on row:', formRow, 'Is last row:', isLastRow, 'Row index:', rowIndex, 'Total rows:', formRows.length);
    console.log(`name: ${event.target.name}`);



    if (event.target.name.includes('skill'))
    {
        console.log('name.includes - skill');
    }



    if (event.target.name.includes('skill_years'))
    {
        console.log('name.includes - skill_years');
    }

    // Validate the row if it's not the last, or if it's the only row
    if (!isLastRow || isOnlyRow) {
        console.log('Validating row:', formRow);
        validateRow(formRow);
    } else {
        console.log('Skipping validation for the last row:', formRow);
    }

    // Handle adding new forms
    if (event.target.name.includes('skill')) {
        // console.log('Skill field changed, adding new form.');
        // addNewForm();

    }




    if (event.target.name.includes('skill_years') || event.target.name.includes('skill_months')) {
        // console.log(event.target.name);
        console.log('101');
        const skillInput = formRow.querySelector('[name$="-skill"]');
        const skillYears = formRow.querySelector('[name$="-skill_years"]').value.trim();
        const skillMonths = formRow.querySelector('[name$="-skill_months"]').value.trim();

        if (skillInput.value.trim() !== '' && (skillYears !== '' || skillMonths !== '')) {
            console.log('Year or month data entered, adding new form.');
            addNewForm();
        }
    }
}

function addNewForm() {
    const formRows = document.querySelectorAll('.form-row');
    const lastForm = formRows[formRows.length - 1];
    const lastSkillInput = lastForm.querySelector('[name$="-skill"]');

    if (formRows.length >= maxForms) {
        return;  // Stop adding new rows if the maximum is reached
    }

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
        updateManagementFormCount();

        // Attach event listeners to inputs in the new row only
        newRow.querySelectorAll('[name$="-skill"], [name$="-skill_years"], [name$="-skill_months"]').forEach(input => {
            input.addEventListener('input', debounce(handleInputEvent, 500));
        });

        printFormRows();
    }
}

function updateManagementFormCount() {
    const formsetContainer = document.getElementById('formset-container');
    const totalForms = formsetContainer.querySelectorAll('.form-row').length;
    const managementForm = formsetContainer.querySelector('input[name$="-TOTAL_FORMS"]');
    if (managementForm) {
        managementForm.value = totalForms;
    }
}

function removeEmptyForms() {
    const formRows = document.querySelectorAll('.form-row');
    formRows.forEach((formRow, index) => {
        const skillInput = formRow.querySelector('[name$="-skill"]');
        if (!skillInput.value.trim()) {
            console.log(`Removing empty form row: ${index}`);
            formRow.remove();
        }
    });
}

function isFormEmpty(formRow) {
    const skillInput = formRow.querySelector('[name$="-skill"]');
    return skillInput && skillInput.value.trim() === '';
}

document.querySelector('form').addEventListener('submit', function(event) {
    console.log('Form submission triggered.');
    removeEmptyForms();
    updateManagementFormCount();
    printFormRows();  // Print the form rows before submission

    // Run validation on all rows before submission
    const formRows = document.querySelectorAll('.form-row');
    let allValid = true;
    formRows.forEach(formRow => {
        if (!validateRow(formRow)) {
            allValid = false;
        }
    });

    if (!allValid) {
        console.log('Form contains validation errors. Submission prevented.');
        event.preventDefault(); // Prevent the form from submitting if validation fails
    }
});

// Attach event listeners to existing skill, skill_years, and skill_months inputs once on initial load
document.querySelectorAll('[name$="-skill"], [name$="-skill_years"], [name$="-skill_months"]').forEach(input => {
    input.addEventListener('input', debounce(handleInputEvent, 500));  // Adjust the delay as needed
});
