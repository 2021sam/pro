// Handling the decision button clicks
document.querySelectorAll('.decision-btn').forEach(button => {
  button.addEventListener('click', function() {
    const jobId = this.dataset.job;
    const freelancerId = this.dataset.freelancer;
    const decision = this.dataset.decision;

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
      }
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