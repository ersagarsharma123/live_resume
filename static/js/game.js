
// Function to update running instances
function updateRunningInstances() {
    fetch('/api/game-status')
        .then(response => response.json())
        .then(data => {
            runningInstancesList.innerHTML = '';
            Object.entries(data).forEach(([mobile, instance]) => {
                if (instance.status === 'running') {
                    const instanceDiv = document.createElement('div');
                    instanceDiv.className = 'instance-item';
                    
                    const infoDiv = document.createElement('div');
                    infoDiv.className = 'instance-info';
                    infoDiv.innerHTML = `
                        <div class="mobile-number"><strong>Mobile:</strong> ${mobile}</div>
                        <div class="target"><strong>Target:</strong> ${instance.target}</div>
                        <div class="balance"><strong>Balance:</strong> ${instance.current_balance}</div>
                        <div class="balance"><strong>Desired-Target:</strong> ${instance.desired_target}</div>
                    `;
                    
                    const stopBtn = document.createElement('button');
                    stopBtn.className = 'instance-stop-btn';
                    stopBtn.textContent = 'Stop';
                    stopBtn.onclick = async () => {
                        try {
                            const response = await fetch('/api/stop-game', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify({ mobile_number: mobile })
                            });
                            if (!response.ok) {
                                throw new Error('Failed to stop instance');
                            }
                            updateRunningInstances();
                        } catch (error) {
                            console.error('Error stopping instance:', error);
                        }
                    };
                    
                    instanceDiv.appendChild(infoDiv);
                    instanceDiv.appendChild(stopBtn);
                    runningInstancesList.appendChild(instanceDiv);
                }
            });
        })
        .catch(error => console.error('Error fetching running instances:', error));
}


document.addEventListener('DOMContentLoaded', function() {
    const startBtn = document.getElementById('startGameBtn');
    const stopBtn = document.getElementById('stopGameBtn');
    const statusText = document.getElementById('statusText');
    const currentTarget = document.getElementById('currentTarget');
    const runningInstancesList = document.getElementById('runningInstancesList');
    let gameWorker = null;

    // Function to update running instances
    function updateRunningInstances() {
        fetch('/api/game-status')
            .then(response => response.json())
            .then(data => {
                runningInstancesList.innerHTML = ''; // Clear existing instances
                Object.entries(data).forEach(([mobile, instance]) => {
                    if (instance.status === 'running') {
                        const instanceDiv = document.createElement('div');
                        instanceDiv.className = 'instance-item';

                        const infoDiv = document.createElement('div');
                        infoDiv.className = 'instance-info';
                        infoDiv.innerHTML = `
                            <div class="mobile-number"><strong>Mobile:</strong> ${mobile}</div>
                            <div class="target"><strong>Target:</strong> ${instance.target}</div>
                            <div class="balance"><strong>Balance:</strong> ${instance.current_balance}</div>
                            <div class="balance"><strong>Desired-Target::</strong> ${instance.desired_target}</div>
                        `;

                        const stopBtn = document.createElement('button');
                        stopBtn.className = 'instance-stop-btn';
                        stopBtn.textContent = 'Stop';
                        stopBtn.onclick = async () => {
                            try {
                                const response = await fetch('/api/stop-game', {
                                    method: 'POST',
                                    headers: {
                                        'Content-Type': 'application/json',
                                    },
                                    body: JSON.stringify({ mobile_number: mobile })
                                });
                                if (!response.ok) {
                                    throw new Error('Failed to stop instance');
                                }
                                updateRunningInstances();
                            } catch (error) {
                                console.error('Error stopping instance:', error);
                            }
                        };

                        instanceDiv.appendChild(infoDiv);
                        instanceDiv.appendChild(stopBtn);
                        runningInstancesList.appendChild(instanceDiv);
                    }
                });
            })
            .catch(error => console.error('Error fetching running instances:', error));
    }

    function startGameWorker(mobileNumber) {
        if (gameWorker) {
            gameWorker.terminate();
        }

        gameWorker = new Worker('/static/js/game-worker.js');
        gameWorker.postMessage({
            type: 'start',
            mobileNumber: mobileNumber
        });

        gameWorker.onmessage = function(e) {
            if (e.data.type === 'status') {
                updateGameStatusUI(e.data.status);
            }
        };
    }

    function updateGameStatusUI(status) {
        if (status) {
            currentTarget.textContent = `Target: ${status.target}`;
            statusText.textContent = `Status: ${status.status}`;
        }
    }

    startBtn.addEventListener('click', async () => {
        const formData = {
            mobile_number: document.getElementById('mobileNumber').value,
            password: document.getElementById('password').value,
            amounts: document.getElementById('amounts').value.split(',').map(amount => amount.trim()),
            set_target: parseFloat(document.getElementById('setTarget').value),
            loss: parseFloat(document.getElementById('loss').value)
        };

        try {
            statusText.textContent = 'Status: Starting game...';
            const response = await fetch('/api/start-game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error('Failed to start game');
            }

            const data = await response.json();
            statusText.textContent = 'Status: Game running';
            currentTarget.textContent = `Target: ${data.final_target}`;
            
            startBtn.disabled = true;
            stopBtn.disabled = false;

            startGameWorker(formData.mobile_number);

        } catch (error) {
            statusText.textContent = `Status: Error - ${error.message}`;
            console.error('Error:', error);
        }
    });

    stopBtn.addEventListener('click', async () => {
        try {
            const mobileNumber = document.getElementById('mobileNumber').value;
            
            const response = await fetch('/api/stop-game', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ mobile_number: mobileNumber })
            });
    
            if (!response.ok) {
                throw new Error('Failed to stop game');
            }
    
            const data = await response.json();
            statusText.textContent = 'Status: Game stopped';
            currentTarget.textContent = 'Target: 0';
            
            startBtn.disabled = false;
            stopBtn.disabled = true;

            if (gameWorker) {
                gameWorker.terminate();
            }
    
        } catch (error) {
            statusText.textContent = `Status: Error - ${error.message}`;
            console.error('Error:', error);
        }
    });

    // Update running instances every 5 seconds
    setInterval(updateRunningInstances, 5000);
});