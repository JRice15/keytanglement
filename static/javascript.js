
// Get the current username from the cookies
var user = cookie.get('user');
if (!user) {

  // Ask for the username if there is none set already
  user = prompt('Choose a username:');
  if (!user) {
    alert('We cannot work with you like that!');
  } else {
    // Store it in the cookies for future use
    cookie.set('user', user);
  }
}

var socket = io();


// When the form is submitted
$('form').submit(function (e) {
  // Avoid submitting it through HTTP
  e.preventDefault();

  // Retrieve the message from the user
  var message = $(e.target).find('input').val();

  // Send the message to the server
  socket.emit('message', {
    user: cookie.get('user') || 'Anonymous',
    message: message
  });

  // Clear the input and focus it for a new message
  e.target.reset();
  $(e.target).find('input').focus();
});

socket.on('prepare message', function(data) {
  $('.chat').append('<p><i><strong>' + data.user + '</strong> is generating a ' + data.msglen + ' bit message </i>')
})

// When we receive a message
// it will be like { user: 'username', message: 'text' }
socket.on('message', function (data) {
  $('.chat').append('<p><strong>' + data.user + '</strong>: ' + data.message + '</p>');
});

// Handle status update
socket.on('status update', function (msg) {
  $('.chat').append('<p><i>... ' + msg + '</i></p>');
});

// Handle status update
socket.on('bad message', function (user) {
  $('.chat').append('<p><i>... ' + user + "'s message is not correctly formatted (must be ASCII)</i></p>");
});

socket.on('attacker', function (user) {
  $('.chat').append('<p><strong>There is an attacker listening!</strong></p>');
});

// join the room if it is a room
if (window.location.pathname.startsWith("/room/")) {
  var roomname = window.location.pathname.split("/")[2]
  socket.emit("join", {
    user: cookie.get('user') || 'Anonymous',
    roomname: roomname
  })
}


// join notice
socket.on('join notice', function (user) {
  $('.chat').append('<p><strong><i>' + user + '</strong> has joined the room</i></p>');
});

