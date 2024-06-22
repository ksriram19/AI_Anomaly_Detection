document.getElementById('loginForm').addEventListener('submit', function (event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById('loggedInUser').textContent = username;
        localStorage.setItem('username', username);
        showSection('dashboard');
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

document.getElementById('logoutButton').addEventListener('click', function () {
    const username = localStorage.getItem('username');

    fetch('/logout', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username }),
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        showSection('logResults');
        displayLogResults(data.log_data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
});

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(section => {
        section.style.display = 'none';
    });
    document.getElementById(sectionId).style.display = 'block';
}

function displayLogResults(logData) {
    const logResultTable = document.getElementById('logResultTable');
    logResultTable.innerHTML = '';
    const row = logResultTable.insertRow();
    Object.values(logData).forEach(text => {
        const cell = row.insertCell();
        cell.textContent = text;
    });
}
