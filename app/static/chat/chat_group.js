let protocol = window.location.protocol === "https:" ? "wss" : "ws"
let url = `${protocol}://${window.location.host}/ws/socket-server/`

const chatSocket = new WebSocket(url)

function build_user_message(data) {
    if (data.author === '{{ user.username }}') {
        return `<div class="row justify-content-start">
                    <div class="row flex-row-reverse">
                        <div class="msg-wrapper-self border rounded p-2 m-1 col-auto">
                            <img style="aspect-ratio: 1/1; width: 32px" src="${data.pfp}" alt="Profile Picture" class="rounded-circle">
                            <span class="fw-bold">From: You</span>
                            <br>
                            <p class="border-top m-0">${data.message}</p>
                        </div>
                    </div>
                </div>`
    }

    return `<div class="row justify-content-start">
                <div class="row">
                    <div class="msg-wrapper border rounded p-2 m-1 col-auto">
                        <img style="aspect-ratio: 1/1; width: 32px" src="${data.pfp}" alt="Profile Picture" class="rounded-circle">
                        <span class="fw-bold">From: ${data.author}</span>
                        <br>
                        <p class="border-top m-0">${data.message}</p>
                    </div>
                </div>
            </div>`
}

function build_notification_message(data) {
    let previous_notification = document.getElementById('chat-notification')
    if (previous_notification !== null) {
        previous_notification.remove()
    }

    if (data.message === 'Someone has just left') {
        return `<div id="chat-notification" class="msg-notification-danger row justify-content-center w-75 border-top my-3 mx-auto pt-2">
                    <p align="center" class="text-danger-emphasis">${data.message}</p>
                </div>`
    }

    return `<div id="chat-notification" class="msg-notification-success row justify-content-center w-75 border-top my-3 mx-auto pt-2">
                <p align="center" class="text-success-emphasis">${data.message}</p>
            </div>`
}

chatSocket.onmessage = function (e) {
    let data = JSON.parse(e.data)
    console.log(data)

    let chat_box = document.querySelector('.message-box')
    let msg_element = null
    if (data.type === 'chat') {
        msg_element = build_user_message(data)
    }
    if (data.type === 'notification') {
        msg_element = build_notification_message(data)

        let counter = document.getElementById('counter')
        counter.innerText = data['user_count'].toString() + ' online'
    }

    chat_box.insertAdjacentHTML('beforeend', msg_element)
    chat_box.scrollTo(0, chat_box.scrollHeight)
}

let chat_form = document.getElementById('chat-form')
chat_form.addEventListener('submit', (e) => {
    e.preventDefault()
    let message = e.target.message.value
    if (message !== '') {
        chatSocket.send(JSON.stringify({
            'author': '{{ user.pk }}',
            'group': '{{ group.pk }}',
            'message': message
        }))
    }
    chat_form.reset()
})