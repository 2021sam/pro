// freelancer_search.js

// Handling the decision button clicks
document.querySelectorAll('.decision-form').forEach(form => {
  form.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission

    const jobId = this.querySelector('input[name="job_id"]').value; // Assuming you have this in your form
    const freelancerId = this.querySelector('input[name="freelancer_id"]').value;
    const decision = this.querySelector('button[type="submit"]').value; // Get the decision from the button

    // Send AJAX POST request to update the decision
    fetch(`/employer/search/update-decision/${jobId}/${freelancerId}/`, {
      method: 'POST',
      headers: {
        'X-CSRFToken': '{{ csrf_token }}', // Make sure CSRF token is included
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: `decision=${decision}`
    })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        alert('Decision updated successfully');
        // Optionally, redirect or refresh the page here if needed
        window.location.href = `/employer/search/search/${jobId}/`; // Redirect to the search page
      } else {
        alert('Error: ' + data.message);
      }
    })
    .catch(error => {
      console.error('Error:', error);
      alert('Error: ' + error);
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
