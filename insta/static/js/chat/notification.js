

document.addEventListener('DOMContentLoaded', function () {
    const websocketNotification = new WebSocket('ws://' + window.location.host + '/ws/notification/');

    websocketNotification.onopen = function () {
        console.log('notification connected');
    }

    websocketNotification.onmessage = function (event) {
        let data = JSON.parse(event.data);
        console.log(data)

        try {
            if (data.type === 'initial_notification_count') {
                console.log('Initial Notification Count:', data.count);
                if (data.count<0) {
                    let count = document.querySelector(`#count-${data.user}`);
                    if (count) {
                        count.textContent = data.count; // Update count if the element exists
                    } else {
                        console.error('Element not found:', `#count-${data.user}`);
                    }
                } else {
                    console.error('User is null or Count is undefined');
                }
            }
            else {
                // Handle other types of messages
                if (data.user > 0) {
                    let countElement = document.querySelector(`#count-${data.user}`);
                    if (countElement) {
                        countElement.textContent = data.count;
                        console.log(countElement)
                    } else {
                        // console.error('Element not found:', `#count-${data.user}`);
                    }
                }
            }
        } catch (error) {
            console.error('Error parsing notification data:', error);
        }
    };

    websocketNotification.onclose = function () {
        console.log('websocket closed');
    }
});




