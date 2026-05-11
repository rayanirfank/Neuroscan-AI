async function uploadMRI() {

    const fileInput = document.getElementById("fileInput");

    const resultBox = document.getElementById("result");

    if (!fileInput.files.length) {

        resultBox.innerHTML = "Please upload an MRI image.";

        return;
    }

    const formData = new FormData();

    formData.append("file", fileInput.files[0]);

    resultBox.innerHTML = "Analyzing MRI image...";

    try {

        const response = await fetch("/upload", {

            method: "POST",

            body: formData

        });

        if (!response.ok) {

            throw new Error("Server error");

        }

        const data = await response.json();

        console.log(data);

        resultBox.innerHTML = `

            <h2>Prediction Result</h2>

            <p><strong>Tumor Type:</strong> ${data.prediction}</p>

            <p><strong>Confidence:</strong> ${data.confidence}%</p>

        `;

    }

    catch (error) {

        console.error(error);

        resultBox.innerHTML = "Error analyzing MRI image.";

    }

}