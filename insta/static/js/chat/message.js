

    // document.addEventListener('DOMContentLoaded', function () {
    //     const user_id = JSON.parse(document.getElementById('json-username').textContent);
    //     const user_message = JSON.parse(document.getElementById('json-message-username').textContent);
    //     const receiver = JSON.parse(document.getElementById('json-username-receiver').textContent);
    //     console.log(user_id)
    //     // const websocket = new WebSocket('ws://' + window.location.host + '/ws/' + user_id + '/');
    //     const websocket = new WebSocket('ws://'+ window.location.host +'/ws/'+ user_id + '/');
        
    //     websocket.onopen = function (e) {
    //         console.log('websocket connected chat');
    //     };
        
    //     websocket.onclose = function (e) {
    //         console.log('connection closed');
    //     };
        
    //     websocket.onerror = function (e) {
    //         console.log(e)
    //         console.log('error');
    //     };
        
    //     websocket.onmessage = function (event) {
    //         let data = JSON.parse(event.data);
    //         console.log(data);
        
    //         let chatBody = document.querySelector('#chat-body');
    //         let messageHtml = '';
        
    //         if (data.message_type === 'text') {
    //             messageHtml = `
    //                 <tr>
    //                     <td>
    //                         <p class="p-2 mt-2 rounded">
    //                             <span class="p-2 text-white rounded bg-primary">${data.message}</span>
    //                         </p>
    //                     </td>
    //                     <td>
    //                         <p><small class="p-1 shadow-sm">${new Date().toLocaleTimeString()}</small></p>
    //                     </td>
    //                 </tr>
    //             `;
    //         } else if (data.message_type === 'image') {
    //             messageHtml = `
    //                 <tr>
    //                     <td>
    //                         <p class="p-2 mt-2 rounded">
    //                             <img src="${data.image}" alt="Image" class="img-fluid p-2 mt-2 rounded">
    //                         </p>
    //                     </td>
    //                     <td>
    //                         <p><small class="p-1 shadow-sm">${new Date().toLocaleTimeString()}</small></p>
    //                     </td>
    //                 </tr>
    //             `;
    //         }
        
    //         chatBody.innerHTML += messageHtml;
    //     };
        
        
    //     // Ensure the element exists before adding the event listener
    //     const sendButton = document.getElementById('send_button');
    //     if (sendButton) {
    //         sendButton.onclick = function (e) {
    //             console.log('Send button clicked');
    //             const message_input = document.getElementById('message_input');
    //             const image_input = document.getElementById('image_input');
    //             const message = message_input.value;
    //             const file = image_input.files[0];
            
    //             if (file) {
    //                 const reader = new FileReader();
    //                 reader.onload = function (e) {
    //                     const image_data = e.target.result;
    //                     websocket.send(JSON.stringify({
    //                         'message': '',
    //                         'username': user_message,
    //                         'receiver': receiver,
    //                         'message_type': 'image',
    //                         'image': image_data
    //                     }));
    //                 };
    //                 reader.readAsDataURL(file);
            
    //                 // Clear the file input
    //                 image_input.value = '';
    //             } else if (message.trim() !== '') {
    //                 websocket.send(JSON.stringify({
    //                     'message': message,
    //                     'username': user_message,
    //                     'receiver': receiver,
    //                     'message_type': 'text'
    //                 }));
            
    //                 const messageTable = document.getElementById('chat-body');
    //                 messageTable.scrollTop = messageTable.scrollHeight;
            
    //                 // Clear the text input
    //                 message_input.value = '';
    //             }
    //         };
    //     } else {
    //         console.error('Send button element not found');
    //     }
        
    //     // Scroll to the bottom when the page is loaded
    //     const cardBody = document.getElementById('card-body');
    //     if (cardBody) {
    //         cardBody.scrollTop = cardBody.scrollHeight;
    //     } else {
    //         console.error('Card body element not found');
    //     }
    // });
    


document.addEventListener('DOMContentLoaded', () => {
    try {
        const user_id = JSON.parse(document.getElementById('json-username').textContent);
        const user_message = JSON.parse(document.getElementById('json-message-username').textContent);
        const receiver = JSON.parse(document.getElementById('json-username-receiver').textContent);

        const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        const websocket = new WebSocket(`${protocol}${window.location.host}/ws/${user_id}/`);

        websocket.addEventListener('open', () => {
            console.log('WebSocket connected');
        });

        websocket.addEventListener('close', () => {
            console.log('WebSocket connection closed');
        });

        websocket.addEventListener('error', (error) => {
            console.error('WebSocket error:', error);
        });

        websocket.addEventListener('message', (event) => {
            const data = JSON.parse(event.data);
            const chatMessages = document.querySelector('.chat-messages');
            if (!chatMessages) return;

            const isSender = data.user === user_message;
            const sideClass = isSender ? 'flex-row-reverse' : '';
            const messageClass = isSender ? 'right-chat-message' : 'left-chat-message';
            const time = new Date().toLocaleTimeString();

            let messageHtml = '';

            if (data.message_type === 'text') {
                messageHtml = `
                    <div class="d-flex ${sideClass} mb-2">
                        <div class="${messageClass} fs-13 mb-2">
                            <div class="mb-0 mr-3 pr-4">
                                <div class="d-flex flex-row">
                                    <div class="pr-2">${data.message}</div>
                                </div>
                            </div>
                            <div class="message-options dark">
                                <div class="message-time">
                                    <div class="d-flex flex-row">
                                        <div class="mr-2">${time}</div>
                                    </div>
                                </div>
                                <div class="message-arrow"><i class="text-muted la la-angle-down fs-17"></i></div>
                            </div>
                        </div>
                    </div>
                `;
            } else if (data.message_type === 'image') {
                messageHtml = `
                    <div class="d-flex ${sideClass} mb-2">
                        <div class="${messageClass} fs-13 mb-2">
                            <div class="mb-0 mr-3 pr-4">
                                <div class="d-flex flex-row">
                                    <img src="${data.image}" alt="Message Image" class="chat-message-image">
                                </div>
                            </div>
                            <div class="message-options dark">
                                <div class="message-time">
                                    <div class="d-flex flex-row">
                                        <div class="mr-2">${time}</div>
                                    </div>
                                </div>
                                <div class="message-arrow"><i class="text-muted la la-angle-down fs-17"></i></div>
                            </div>
                        </div>
                    </div>
                `;
            }

            chatMessages.insertAdjacentHTML('beforeend', messageHtml);
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });

        const sendButton = document.querySelector('.chat-search .input-group .input-group-append');
        const messageInput = document.querySelector('.chat-search input[type="text"]');

        const imageInput = document.getElementById('chat-file-input');
        const uploadTrigger = document.getElementById('chat-upload');

        if (uploadTrigger && imageInput) {
            uploadTrigger.addEventListener('click', () => {
                imageInput.click(); // Trigger the hidden file input
            });
        }

        if (sendButton) {
            sendButton.addEventListener('click', () => {
                if (!websocket || websocket.readyState !== WebSocket.OPEN) {
                    console.warn('WebSocket is not connected.');
                    return;
                }

                const message = messageInput?.value.trim();
                const file = imageInput?.files[0];

                if (file) {
                    const reader = new FileReader();
                    reader.onload = (e) => {
                        const imageData = e.target.result;
                        websocket.send(JSON.stringify({
                            message: '',
                            username: user_message,
                            receiver: receiver,
                            message_type: 'image',
                            image: imageData
                        }));
                    };
                    reader.readAsDataURL(file);
                    imageInput.value = '';
                } else if (message) {
                    websocket.send(JSON.stringify({
                        message: message,
                        username: user_message,
                        receiver: receiver,
                        message_type: 'text'
                    }));
                    messageInput.value = '';
                }
            });
        } else {
            console.error('Send button not found');
        }

        const chatMessages = document.querySelector('.chat-messages');
        if (chatMessages) {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        }

    } catch (err) {
        console.error('Chat initialization error:', err);
    }
});
