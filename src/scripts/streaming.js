// const socket = new WebSocket("ws://localhost:8001/");
const socket = new WebSocket("wss://coherent-classic-platypus.ngrok-free.app");
const imageElement = document.getElementById("stream");
const modalImage = document.getElementById('modalImage');
const imgElement = document.getElementById('stream');
const modal = document.getElementById('imageModal');

imgElement.addEventListener('click', function () {
    modal.classList.add('active');
});

modal.addEventListener('click', function () {
    modal.classList.remove('active');
});

socket.onmessage = function (event) {
    if (modal.classList.contains('active')) {
        modalImage.src = "data:image/jpeg;base64," + event.data;
    } else {
        imageElement.src = "data:image/jpeg;base64," + event.data;
    }
};

socket.onerror = function (error) {
    console.error("WebSocket Error:", error);
    // imageElement.src = 'ok.jpg'
};

socket.onclose = function () {
    console.warn("WebSocket closed. Refresh the page to reconnect.");
};