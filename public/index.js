const sio = io({
  // adding additional params in request
  transportOptions: {
    polling: {
      extraHeaders: {
        // ws doesnt support headers
        'X-Username': window.location.hash.substring(1)
      }
    }
  }
});


sio.on('connect', () => {
  var alert = document.getElementById("alerts")
  alert.innerHTML = "Connected!"
  console.log('connected');
  // sio.emit('add', { numbers: [1, 2, 5] }, res => console.log(res))
});


sio.on('disconnect', (res) => {
  var alert = document.getElementById("alerts")
  alert.innerHTML = "Disconnected!"
  alert.innerHTML = `${res} left the room.`
});

sio.on("user_joined", res => {
  var alert = document.getElementById("alerts")
  alert.innerHTML = `${res} joined the room.`
})

sio.on("user_left", res => {
  var alert = document.getElementById("alerts")
  alert.innerHTML = `${res} left the room.`
})

sio.on("room_count", res => console.log(`Connected clients in ${res[0]}: ${res[1]}`))

sio.on("count", res => console.log(`Connected clients: ${res}`))

sio.on('connect_error', err => console.log(err.message))

sio.on("mult", (data, callback) => {
  [a, b] = data.numbers
  callback(a * b)
})
sio.on('message', data => {
  console.log("DATA", data)
  var messageBox = document.getElementById("message_box")
  messageBox.innerHTML = messageBox.innerHTML +
  `<div class="d-block w-75 my-1 bg-dark p-2 text-white">
    ${data.message}
    </div>`
} )

function sendMessage(e) {
  var username = window.location.hash.substring(1)
  var message = document.getElementById("input_field")
  console.log(message)
  var text = `<b class="text-uppercase">${username}</b>` + ' : ' + message.value
  sio.emit('text', text)
  message.innerHTML == ''
}