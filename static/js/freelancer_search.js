// freelancer_search.js

// Handling the decision button clicks
document.querySelectorAll('.decision-form').forEach(form => {
    form.addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent default form submission

        const jobId = this.querySelector('input[name="job_id"]').value; // Ensure job_id is included
        const freelancerId = this.querySelector('input[name="freelancer_id"]').value;
        const decision = this.querySelector('button[name="decision"]:hover')?.value; // Get the value of the button being hovered over

        // Send AJAX POST request to update the decision
        fetch(`/employer/search/update-decision/${jobId}/${freelancerId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': '{{ csrf_token }}',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `decision=${decision}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                alert('Decision updated successfully');

                // Toggle button color
                const button = this.querySelector(`button[value="${decision}"]`);
                if (button.style.backgroundColor === 'green') {
                    button.style.backgroundColor = ''; // Reset to default color
                } else {
                    button.style.backgroundColor = 'green'; // Set to green
                }
            } else {
                alert(`Error: ${data.message}`);
            }
        })
        .catch(error => {
            alert('Error: ' + error.message);
        });
    });
});




// Handling the rating input change
document.querySelectorAll('.rating-input').forEach(input => {
  input.addEventListener('change', function() {
    const jobId = this.dataset.job;
    const freelancerId = this.dataset.freelancer;
    const rating = this.value;

    // Send AJAX POST request to update the rating
    fetch(`/employer/search/update-rating/${jobId}/${freelancerId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `rating=${rating}`
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        alert('Rating updated successfully');
      } else {
        alert('Error: ' + data.message);
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });
});
