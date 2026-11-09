const canvas = document.getElementById("drawingCanvas");
const context = canvas.getContext("2d");
const clearButton = document.getElementById("clearButton");
const recognizeButton = document.getElementById("recognizeButton");
const result = document.getElementById("result");
const accuracy = document.getElementById("accuracy");
const prediction = document.getElementById("prediction");
const bars = document.getElementById("bars");
const barFills = [];
const barPercents = [];

for (let i = 0; i < 10; i++){
    const row = document.createElement("div");
    row.className = "bar-row";
    row.innerHTML = `
        <span class="bar-digit">${i}</span>
        <div class="bar-track"><div class="bar-fill"></div></div>
        <span class="bar-percent">0%</span>`;
    bars.appendChild(row);
    barFills.push(row.querySelector(".bar-fill"));
    barPercents.push(row.querySelector(".bar-percent"));
}

function showbars(probabilities, best){
    probabilities.forEach((p, i) => {
        barFills[i].style.width = (p * 100) + "%";
        barFills[i].classList.toggle("top", i === best);
        barPercents[i].textContent = (p * 100).toFixed(0) + "%";
    });
}

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

canvas.addEventListener("pointermove", (event) => {
    if (!isdrawing) return;
    context.lineTo(event.offsetX, event.offsetY);
    context.stroke();
});

canvas.addEventListener("pointerup", () => {
    isdrawing = false;
});

canvas.addEventListener("pointercancel", () => {
    isdrawing = false;
});

clearButton.addEventListener("click", () => {
    context.clearRect(0, 0, canvas.width, canvas.height);
    context.fillStyle = "white";
    context.fillRect(0, 0, canvas.width, canvas.height);
    prediction.textContent = "--";
    accuracy.textContent = "--%";
    result.textContent = "Your prediction will appear here.";
    showbars(new Array(10).fill(0), -1);
});

recognizeButton.addEventListener("click", async () => {
    recognizeButton.textContent = "Recognizing...";
    recognizeButton.disabled = true;
    try {
        const image = await new Promise(resolve => {
            canvas.toBlob(resolve, "image/png");
        });
        const formData = new FormData();
        formData.append("image", image, "drawing.png");
        const reply = await fetch("/predict", {
            method: "POST",
            body: formData
        });
        const data = await reply.json();
        console.log(data);

        if (data.prediction !== undefined){
            prediction.textContent = data.prediction;
            accuracy.textContent = (data.accuracy * 100).toFixed(1) + "%";
            result.textContent = "Your prediction will appear here.";
            showbars(data.probabilities, data.prediction);
        }
        else{
            result.textContent = `Error: ${data.error}`;
        }
    }
    catch (error){
        result.textContent = `Error: ${error.message}`;
    }
    finally {
        recognizeButton.textContent = "Recognize";
        recognizeButton.disabled = false;
    }
});