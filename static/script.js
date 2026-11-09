const canvas = document.getElementById("drawingCanvas");
const context = canvas.getContext("2d");
const clearButton = document.getElementById("clearButton");
const recognizeButton = document.getElementById("recognizeButton");
const result = document.getElementById("result");
const accuracy = document.getElementById("accuracy")
const prediction = document.getElementById("prediction")

context.lineWidth = 9;
context.lineCap = "round";
context.strokeStyle = "black";
context.lineJoin = "round";
context.fillStyle = "white";
context.fillRect(0, 0, canvas.width, canvas.height);

let isdrawing = false;

canvas.addEventListener("pointerdown", (event) => {
    isdrawing = true;
    context.beginPath();
    context.moveTo(event.offsetX, event.offsetY);
});

canvas.addEventListener("pointermove", (event) =>{
    if (!isdrawing) return;
    context.lineTo(event.offsetX, event.offsetY);
    context.stroke();
});

canvas.addEventListener("pointerup", (event) => {
    isdrawing = false;
});

canvas.addEventListener("pointercancel", (event) =>{
    isdrawing = false;
});

clearButton.addEventListener("click", () => {
    context.clearRect(0, 0, canvas.width, canvas.height)
    context.fillStyle = "white";
    context.fillRect(0, 0, canvas.width, canvas.height);
});

recognizeButton.addEventListener("click", async() =>{
    recognizeButton.textContent = "Recognizing...";
    recognizeButton.disabled = true;
    try{
        const image = await new Promise(resolve => {
            canvas.toBlob(resolve, "image/png");
        });
        const formData = new FormData();
        formData.append("image", image, "drawing.png");
        const reply = await fetch("/predict", {
            method: 'POST',
            body: formData
        });
        const data = await reply.json();
        console.log(data);
        if (data.prediction !== undefined){
            prediction.textContent = data.prediction;
            accuracy.textContent = (data.accuracy * 100).toFixed(1) + "%";
        }
        else{
            result.textContext = `Error: ${data.error}`;
        }
    }
    finally{
        recognizeButton.textContent = "Recognize";
        recognizeButton.disabled = false;
    }
});