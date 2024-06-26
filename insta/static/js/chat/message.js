    
    // const user_name = JSON.parse(document.getElementById('json-username').textContent)
    // const user_message = JSON.parse(document.getElementById('json-message-username').textContent)
    // const receiver = JSON.parse(document.getElementById('json-username-receiver').textContent)
    // // console.log(user_name)
    // // console.log(receiver)
    
    // const websocket = new WebSocket('ws://' + window.location.host +'/ws/'+ user_name + '/');
    // // const wb = new WebSocket('ws://127.0.0.1:8000/ws/sc/' + group_name + '/');


    // websocket.onopen = function(e){
    //     console.log('websocket connected chat')
    // }

    // websocket.onclose = function(e){
    //     console.log('conection closed')
    // }

    // websocket.onerror = function(e){
    //     console.log('error',)
    // }

    // websocket.onmessage = function(event){
    //     // console.log('message',event)
    //     // console.log(event.data)
    //     let data = JSON.parse(event.data)
    //     console.log(data.username,'user')
    //     console.log(data.receiver,'receiver')

    // if (data.username) {
    //     document.querySelector('#chat-body').innerHTML += `
    //     <tr>
    //         <td>
    //             <p class="p-2 mt-2 rounded">
    //                 <span class="bg-primary p-2 text-white rounded">${data.message}</span>
    //             </p>
    //         </td>
    //     </tr>
    // `;
    // } else {
    //     document.querySelector('#chat-body').innerHTML += `
    //         <tr>
    //             <td> 
    //                 <p p-2 mt-2 rounded">
    //                     <span class="bg-success p-2 text-white rounded">${data.message}</span>
    //                 </p>
    //             </td>
    //         </tr>
    //     `;
    // }

    // }

    // document.getElementById('send_button').onclick = function(e) {
    //     console.log('button xlick')
    //     let message_input = document.getElementById('message_input');
    //     const message = message_input.value;

    //     if (message.trim() !== '') {
    //         websocket.send(JSON.stringify({
    //             'message': message,
    //             'username': user_message,
    //             'receiver' :receiver
    //         }));

    //         const messageTable = document.getElementById('chat-body');
    //         messageTable.scrollTop = messageTable.scrollHeight;
    //     }

    //     message_input.value = '';
    //     $("#card-body").animate({ scrollTop: 20000000 }, "slow")
    // };

    // // Scroll to the bottom when the page is loaded
    // document.addEventListener("DOMContentLoaded", function () {
    //     const messageTable = document.getElementById('card-body');
    //     messageTable.scrollTop = messageTable.scrollHeight;
    // });



    document.addEventListener('DOMContentLoaded', function () {
        const user_name = JSON.parse(document.getElementById('json-username').textContent);
        const user_message = JSON.parse(document.getElementById('json-message-username').textContent);
        const receiver = JSON.parse(document.getElementById('json-username-receiver').textContent);
        
        const websocket = new WebSocket('ws://' + window.location.host + '/ws/' + user_name + '/');
        
        websocket.onopen = function (e) {
            console.log('websocket connected chat');
        };
        
        websocket.onclose = function (e) {
            console.log('connection closed');
        };
        
        websocket.onerror = function (e) {
            console.log('error');
        };
        
        websocket.onmessage = function (event) {
            let data = JSON.parse(event.data);
            console.log(data);
        
            let chatBody = document.querySelector('#chat-body');
            let messageHtml = '';
        
            if (data.message_type === 'text') {
                messageHtml = `
                    <tr>
                        <td>
                            <p class="p-2 mt-2 rounded">
                                <span class="p-2 text-white rounded bg-primary">${data.message}</span>
                            </p>
                        </td>
                        <td>
                            <p><small class="p-1 shadow-sm">${new Date().toLocaleTimeString()}</small></p>
                        </td>
                    </tr>
                `;
            } else if (data.message_type === 'image') {
                messageHtml = `
                    <tr>
                        <td>
                            <p class="p-2 mt-2 rounded">
                                <img src="${data.image}" alt="Image" class="img-fluid p-2 mt-2 rounded">
                            </p>
                        </td>
                        <td>
                            <p><small class="p-1 shadow-sm">${new Date().toLocaleTimeString()}</small></p>
                        </td>
                    </tr>
                `;
            }
        
            chatBody.innerHTML += messageHtml;
        };
        
        
        // Ensure the element exists before adding the event listener
        const sendButton = document.getElementById('send_button');
        if (sendButton) {
            sendButton.onclick = function (e) {
                console.log('Send button clicked');
                const message_input = document.getElementById('message_input');
                const image_input = document.getElementById('image_input');
                const message = message_input.value;
                const file = image_input.files[0];
            
                if (file) {
                    const reader = new FileReader();
                    reader.onload = function (e) {
                        const image_data = e.target.result;
                        websocket.send(JSON.stringify({
                            'message': '',
                            'username': user_message,
                            'receiver': receiver,
                            'message_type': 'image',
                            'image': image_data
                        }));
                    };
                    reader.readAsDataURL(file);
            
                    // Clear the file input
                    image_input.value = '';
                } else if (message.trim() !== '') {
                    websocket.send(JSON.stringify({
                        'message': message,
                        'username': user_message,
                        'receiver': receiver,
                        'message_type': 'text'
                    }));
            
                    const messageTable = document.getElementById('chat-body');
                    messageTable.scrollTop = messageTable.scrollHeight;
            
                    // Clear the text input
                    message_input.value = '';
                }
            };
        } else {
            console.error('Send button element not found');
        }
        
        // Scroll to the bottom when the page is loaded
        const cardBody = document.getElementById('card-body');
        if (cardBody) {
            cardBody.scrollTop = cardBody.scrollHeight;
        } else {
            console.error('Card body element not found');
        }
    });
    