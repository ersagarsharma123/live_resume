self.onmessage = function(e) {
    if (e.data.type === 'start') {
        const mobileNumber = e.data.mobileNumber;
        
        // Simulate game logic running in background
        function updateStatus() {
            // You would replace this with actual game status updates
            fetch('/api/game-status')
                .then(response => response.json())
                .then(data => {
                    const status = data[mobileNumber];
                    if (status) {
                        self.postMessage({
                            type: 'status',
                            status: status
                        });
                    }
                })
                .catch(error => console.error('Error in worker:', error));
        }

        // Update status periodically
        setInterval(updateStatus, 2000);
    }
};