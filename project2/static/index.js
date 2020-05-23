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

    // When a new vote is announced, add to the unordered list
    socket.on('channels', data => {
        // if (data.channelconnected == connectedChannel()) {
        // var connectedChannel = 0
        // var items = document.querySelectorAll(".btn-outline-success");
        // if (items.length > 0)
        //     connectedChannel = parseInt(items[0].dataset.code);

        document.querySelector('#channels').innerHTML = '';

        data.forEach(element => {
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


        // if (connectedChannel != 0)
        //     document.querySelectorAll(".btn.btn-sm.btn-outline-secondary")[connectedChannel].className = "btn btn-outline-success";

        // let items2 = document.querySelectorAll(".btn-outline-success");
        // if (items2.length == 0)
        //     document.querySelectorAll(".btn.btn-sm.btn-outline-secondary")[0].className = "btn btn-outline-success";

    });

    socket.on('messages', data => {
        let messages = [];
        data.forEach(element => {
            if (element.name == window.localStorage.currentChannel)
                messages = element.messages;
        });

        document.querySelector('#messages').innerHTML = '';

        messages.forEach(element => {
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
    }

    document.querySelector('#txtmessage').onkeyup = (event) => {
        if (event.keyCode === 13) {
            let message = document.querySelector('#txtmessage').value;
            socket.emit('send message', { 'channel': window.localStorage.currentChannel, 'message': message })
            document.querySelector('#txtmessage').value = '';
        }
    }

    scrollToBottom();
});