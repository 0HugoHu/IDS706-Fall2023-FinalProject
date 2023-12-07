// $(document).ready(function () {
//     // Function to fetch messages from the server
//     function fetchMessages() {
//         $.ajax({
//             url: '/get_messages',  // Replace with your Flask route
//             method: 'GET',
//             success: function (data) {
//                 displayMessages(data.messages);  // Assuming 'messages' is an array in the returned data
//             },
//             error: function (error) {
//                 console.error('Error fetching messages:', error);
//             }
//         });
//     }
//
//     // Function to display messages in the chat container
//     function displayMessages(messages) {
//         var chatContainer = $('#chat-container');
//
//         // Clear existing messages
//         chatContainer.empty();
//
//         // Append each message to the chat container
//         messages.forEach(function (message) {
//             var messageClass = message.incoming ? 'incoming' : 'outgoing';
//             var messageHTML = '<div class="message ' + messageClass + '"><p>' + message.text + '</p></div>';
//             chatContainer.append(messageHTML);
//         });
//
//         // Scroll to the bottom of the chat container
//         chatContainer.scrollTop(chatContainer[0].scrollHeight);
//     }
//
//     // Function to send a message to the server
//     function sendMyMessage() {
//         var messageInput = $('#message-input');
//         var messageText = messageInput.val();
//
//         if (messageText.trim() !== '') {
//             $.ajax({
//                 url: '/send_message',  // Replace with your Flask route for sending messages
//                 method: 'POST',
//                 data: { message: messageText },
//                 success: function () {
//                     // Fetch messages again after sending a new message
//                     fetchMessages();
//                     // Clear the input box
//                     messageInput.val('');
//                 },
//                 error: function (error) {
//                     console.error('Error sending message:', error);
//                 }
//             });
//         }
//     }
//
//     // Fetch messages initially and set up periodic refresh
//     fetchMessages();
//     setInterval(fetchMessages, 3000);  // Fetch messages every 3 seconds (adjust as needed)
// });
