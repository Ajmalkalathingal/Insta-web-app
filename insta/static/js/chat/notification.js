const websocketNotification = new WebSocket('ws://' + window.location.host + '/ws/notification/');

websocketNotification.onopen = function () {
    console.log('Notification WebSocket connected');
};

document.addEventListener('DOMContentLoaded', function () {
    websocketNotification.onmessage = function (event) {
        let data = JSON.parse(event.data);
        console.log('Received notification:', data);

        const countElement = document.getElementById(`count-${data.user}`);
        const countElementZero = document.getElementById(`countzero-${data.user}`);

        if (countElement) {
            countElement.innerText = data.count;
            countElement.style.display = data.count > 0 ? 'inline-block' : 'none';
        } else if (countElementZero) {
            countElementZero.innerText = data.count;
            countElementZero.style.display = data.count > 0 ? 'inline-block' : 'none';
        } else {
            console.warn(`No element found for user ID: ${data.user}`);
        }
    };
});

websocketNotification.onclose = function () {
    console.log('Notification WebSocket closed');
};
