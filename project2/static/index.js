window.localStorage.currentChannel = "GENERAL"

function scrollToBottom() {
    let scrollingElement = (document.scrollingElement || document.body);
    scrollingElement.scrollTop = scrollingElement.scrollHeight;
}


document.addEventListener('DOMContentLoaded', function () {

    let socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {
        socket.emit('create channel', { 'channel': '' });
        socket.emit('send message', { 'channel': '', 'message': '' });
    });

    socket.on('channels', data => {
        document.querySelector('#channels').innerHTML = '';

        data.forEach(element => {
            if (!window.localStorage.currentChannel)
                window.localStorage.currentChannel = element.name;

            document.querySelector('#channels').insertAdjacentHTML('beforeend',
                '<button class="btn btn-sm btn-outline-secondary" type="button" id="channel_' + element.name + '">' + element.name + '</button>');

            document.querySelector("#channel_" + element.name).onclick = () => {
                window.localStorage.currentChannel = element.name;

                let items = document.querySelectorAll("[id^='channel_']");
                items.forEach(element => {
                    element.className = "btn btn-sm btn-outline-secondary";
                });

                document.querySelector("#channel_" + element.name).className = "btn btn-outline-success";

                socket.emit('send message', { 'channel': '', 'message': '' });
            }
        });

        let currentChannel = window.localStorage.currentChannel;
        if (currentChannel)
            document.querySelector("#channel_" + currentChannel).className = "btn btn-outline-success";
        else
            document.querySelectorAll("[id^='channel_']")[0].className = "btn btn-outline-success";

        socket.emit('send message', { 'channel': '', 'message': '' });
    });

    socket.on('messages', data => {
        let messages = [];
        data.forEach(element => {
            if (element.name == window.localStorage.currentChannel)
                messages = element.messages;
        });

        document.querySelector('#messages').innerHTML = '';

        messages.forEach(element => {
            var filter = document.querySelector("#txtsearch").value;
            if (element.text.includes(filter))
                document.querySelector('#messages').insertAdjacentHTML('beforeend', '<table class="message"><tr><td>' + element.sender + '</td></tr><tr><td>' + element.text + '</td></tr></table>');
        });

        scrollToBottom();
    });

    document.querySelector('#txtchannel').onkeyup = (event) => {
        if (event.keyCode === 13) {
            socket.emit('create channel', { 'channel': document.querySelector('#txtchannel').value })
            document.querySelector('#txtchannel').value = '';
        }
    }

    document.querySelector('#btnsend').onclick = () => {
        let message = document.querySelector('#txtmessage').value;
        socket.emit('send message', { 'channel': window.localStorage.currentChannel, 'message': message })
        document.querySelector('#txtmessage').value = '';
        document.querySelector('#txtsearch').value = '';
    }

    document.querySelector('#txtmessage').onkeyup = (event) => {
        if (event.keyCode === 13) {
            let message = document.querySelector('#txtmessage').value;
            socket.emit('send message', { 'channel': window.localStorage.currentChannel, 'message': message })
            document.querySelector('#txtmessage').value = '';
            document.querySelector('#txtsearch').value = '';
        }
    }

    document.querySelector('#txtsearch').onkeyup = (event) => {
        if (event.keyCode === 13) {
            socket.emit('send message', { 'channel': '', 'message': '' });
        }
    }

    scrollToBottom();
});