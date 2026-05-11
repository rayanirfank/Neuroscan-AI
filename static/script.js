console.log("script loaded");

const uploadBtn = document.getElementById("uploadBtn");

const uploadInput = document.getElementById("fileInput");

const resultBox = document.getElementById("result");

const previewImage = document.getElementById("previewImage");

uploadBtn.onclick = function () {

    uploadInput.click();

};

uploadInput.onchange = async function () {

    console.log("file selected");

    const file = this.files[0];

    if (!file) return;

    // Display uploaded image instantly

    const imageURL = URL.createObjectURL(file);

    previewImage.src = imageURL;

    // Prepare upload

    const formData = new FormData();

    formData.append("file", file);

    resultBox.innerHTML = "Analyzing MRI Scan...";

    try {

const response = await fetch(
    "/upload",
    {
        method: "POST",
        body: formData
    }
);

        const data = await response.json();

        resultBox.innerHTML = `

            <h2>Prediction: ${data.prediction}</h2>

            <p>Confidence: ${data.confidence}%</p>

        `;

        console.log(data);

    }

    catch (error) {

        console.error(error);

        resultBox.innerHTML = "Error analyzing MRI image.";

    }

};