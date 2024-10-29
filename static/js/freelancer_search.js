// Handling the decision button clicks
document.querySelectorAll('.decision-form').forEach(form => {
  form.addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the default form submission

    const jobId = this.querySelector('input[name="job_id"]').value;  // Assuming you have a hidden input for job_id
    const freelancerId = this.querySelector('input[name="freelancer_id"]').value;
    const decision = this.querySelector('button[type="submit"]').value;

    // Send AJAX POST request to update the decision
    fetch(`/employer/search/update-decision/${jobId}/${freelancerId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': '{{ csrf_token }}',  // Use the Django CSRF token
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `decision=${decision}`
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        alert('Decision updated successfully');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('An error occurred while updating the decision.');
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
    fetch(`/employer/search/update-decision/${jobId}/${freelancerId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': '{{ csrf_token }}',
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `rating=${rating}`
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        alert('Rating updated successfully');
      }
    });
  });
});
