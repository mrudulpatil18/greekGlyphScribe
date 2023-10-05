const Canvas = () => {
    var canvas = document.querySelector("#canvas");
    var context = canvas.getContext("2d");
    canvas.width = 280;
    canvas.height = 280;

    var Mouse = { x: 0, y: 0 };
    var lastMouse = { x: 0, y: 0 };
    context.fillStyle = "white";
    context.fillRect(0, 0, canvas.width, canvas.height);
    context.color = "black";
    context.lineWidth = 22;
    context.lineJoin = context.lineCap = 'round';

    debug();

    canvas.addEventListener("mousemove", function (e) {
        lastMouse.x = Mouse.x;
        lastMouse.y = Mouse.y;

        Mouse.x = e.pageX - this.offsetLeft - 15;
        Mouse.y = e.pageY - this.offsetTop - 15;
    }, false);

    canvas.addEventListener("mousedown", function (e) {
        canvas.addEventListener("mousemove", onPaint, false);
    }, false);

    canvas.addEventListener("mouseup", function () {
        canvas.removeEventListener("mousemove", onPaint, false);
    }, false);

    var onPaint = function () {
        context.lineWidth = context.lineWidth;
        context.lineJoin = "round";
        context.lineCap = "round";
        context.strokeStyle = context.color;

        context.beginPath();
        context.moveTo(lastMouse.x, lastMouse.y);
        context.lineTo(Mouse.x, Mouse.y);
        context.closePath();
        context.stroke();
    };

    function debug() {
        const clear = document.querySelector('#clearButton')
        clear.addEventListener("click", () => {
            context.clearRect(0, 0, 280, 280);
            context.fillStyle = "white";
            context.fillRect(0, 0, canvas.width, canvas.height);
        })
    }
};

Canvas();


document.querySelector(".myButton").addEventListener("click", async function() {
    document.querySelector('.result').textContent = 'Predicting...';

    const canvasObj = document.getElementById("canvas");
    const img = canvasObj.toDataURL('image/png');
    try {
        const response = await fetch('/predict/', {
            method: 'POST',
            body: img,
            headers: {
                'Content-Type': 'image/png'
            }
        });
        
        if (response.ok) {
            const data = await response.text()
            document.querySelector('.result').innerHTML = 
            `
            <a href="https://en.wikipedia.org/wiki/${JSON.parse(data)[0].Name}" target="_blank">
            <div class="card hover">
                <div class="heading"> 	\\(${ JSON.parse(data)[0].LaTeX }\\)
                    <div class="author"> Confidence <span class="name"> \\(${JSON.parse(data)[0].Confidence.toFixed(1)}\\) %</span></div>
                </div>
                <div class="category"> \\(${JSON.parse(data)[0].Name}\\) </div>
            </div>
            </a>

            <a href="https://en.wikipedia.org/wiki/${JSON.parse(data)[1].Name}" target="_blank">
            <div class="card hover">
                <div class="heading"> 	\\(${ JSON.parse(data)[1].LaTeX }\\)
                    <div class="author"> Confidence <span class="name"> \\(${JSON.parse(data)[1].Confidence.toFixed(1)}\\) %</span></div>
                </div>
                <div class="category"> \\(${JSON.parse(data)[1].Name}\\) </div>
            </div>
            </a>


            <a href="https://en.wikipedia.org/wiki/${JSON.parse(data)[2].Name}" target="_blank">
            <div class="card hover">
                <div class="heading"> 	\\(${ JSON.parse(data)[2].LaTeX }\\)
                    <div class="author"> Confidence <span class="name"> \\(${JSON.parse(data)[2].Confidence.toFixed(1)}\\) %</span></div>
                </div>
                <div class="category"> \\(${JSON.parse(data)[2].Name}\\) </div>
            </div>
            </a>
            `;
            // document.querySelector('#result').innerHTML = '\\(' + JSON.parse(data)[1].LaTeX + '\\)';
            // document.querySelector('#result').innerHTML = '\\(' + JSON.parse(data)[2].LaTeX + '\\)';
            MathJax.typesetPromise();
        } else {
            document.querySelector('#result').textContent = 'Prediction failed.';
        }
    } catch (error) {
        console.error('Error:', error);
        document.querySelector('#result').textContent = 'An error occurred.';
    }
});
