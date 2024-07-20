document.getElementById('analyze-btn').addEventListener('click', function() {
    const code = document.getElementById('code-input').value;

    fetch('/analyze', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: code })
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert('Error: ' + data.error);
        } else {
            document.getElementById('time-complexity').innerText = 'Time Complexity: ' + data.time_complexity;
            document.getElementById('space-complexity').innerText = 'Space Complexity: ' + data.space_complexity;
            document.getElementById('pylint-report').innerText = data.pylint_report;
        }
    })
    .catch(error => {
        alert('Error: ' + error);
    });
});
