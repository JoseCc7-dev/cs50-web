var url = window.location.href.slice(0, -3)

document.addEventListener("DOMContentLoaded", function() {
    
    const chatbox = document.querySelector("#chat-content")
    chatbox.scrollTop = chatbox.scrollHeight
    
})

function send_message(message, user) {
    // fetch call to py view save new msg
    csrftoken = document.getElementsByName('csrfmiddlewaretoken')[0].value
    room = document.getElementById("room-name").innerHTML
    fetch('/send' , {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            text: message,
            room: room,
            user: user
        })
      })
      .then(response => response.json())
}

function update_chat(message, user) {
    // update chat with new message
    const chatbox = document.querySelector("#chat-content")
    const div = document.createElement('div')
    const innerdiv = document.createElement('div')
    const p1 = document.createElement('p')
    const p2 = document.createElement('p')
    const curruser = document.querySelector("#curruser").innerHTML
    
    
    innerdiv.className = "media-body"
    p1.className = "meta"
    p1.style.color = "#9b9b9b"
    p1.innerHTML = user
    p2.innerHTML = message

    // Place div on right or left side
    div.className = "media media-chat "
    if (curruser == user) {
        div.className += "media-chat-reverse"
        innerdiv.append(p1, p2)
    }
    else {
        var img = document.createElement('img')
        var p3 = document.createElement('p')

        img.className = "avatar"
        img.src = url + "static/chatroom/pfp1.jpg"
        p3.innerHTML = moment(Date()).format('MMMM D, YYYY, h:mm a')
        p3.className = "meta"

        div.append(img)
        innerdiv.append(p1, p2, p3)
    }
    
    div.append(innerdiv)
    chatbox.append(div)
    // Scroll to Bottom of Chat
    chatbox.scrollTop = chatbox.scrollHeight
    // Reset input field and set focus
    const user_message = document.querySelector("#new_message")
    user_message.value = ""
    user_message.focus()
    return false
}