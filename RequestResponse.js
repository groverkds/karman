function submitonenter(evt, thisObj) {
    evt = (evt) ? evt : ((window.event) ? window.event : "")
    if (evt) {
        if (evt.keyCode == 13 || evt.which == 13) {
            getResponse();
        }
    }
}
function getResponse() {
    var conv = document.getElementById('conversation');
    var msgholder = document.createElement('div');
    msgholder.className = 'message-box-holder';
    conv.appendChild(msgholder);
    var msg = document.createElement('div');
    msg.className = 'message-box';
    msg.innerHTML = document.getElementById('clientmessage').value;
    msgholder.appendChild(msg);
    var objDiv = document.getElementById("conversation");
    objDiv.scrollTop = objDiv.scrollHeight;

    console.log(msg.innerHTML);
    document.getElementById('clientmessage').value = '';
    var xhr = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/chat/?query=" + encodeURIComponent(msg.innerHTML);
    console.log(url);
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Cntent-Type", "application/x-www-form-urlencoded");
    xhr.send();

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            console.log(xhr.responseText);
            var json = JSON.parse(xhr.responseText);
            var msgholder1 = document.createElement('div');
            msgholder1.className = 'message-box-holder';
            conv.appendChild(msgholder1);
            var msg1 = document.createElement('div');
            msg1.className = "message-box message-partner";
            msg1.innerHTML = json['reply'];
            msgholder1.appendChild(msg1);
            var objDiv = document.getElementById("conversation");
            objDiv.scrollTop = objDiv.scrollHeight;

        }
    }
}    