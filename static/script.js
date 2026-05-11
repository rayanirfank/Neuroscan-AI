async function uploadMRI() {
    const fileInput = document.getElementById("fileInput");
    const resultBox = document.getElementById("result");
    const previewImage = document.getElementById("previewImage");

    if (fileInput.files.length === 0) {
        resultBox.innerHTML = "Please select an MRI image.";
        return;
    }

    const selectedFile = fileInput.files[0];

    const imageURL = URL.createObjectURL(selectedFile);
    previewImage.src = imageURL;

    const formData = new FormData();
    formData.append("file", selectedFile);

    resultBox.innerHTML = "Analyzing MRI image... (this may take up to 2 minutes on first load)";

    // Timeout controller — 3 minutes
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 180000);

    try {
        const response = await fetch("/upload", {
            method: "POST",
            body: formData,
            signal: controller.signal
        });

        clearTimeout(timeoutId);

        if (!response.ok) {
            throw new Error("Upload failed");
        }

        const data = await response.json();
        console.log(data);

        resultBox.innerHTML = `
            <h2>Prediction Result</h2>
            <p><strong>Tumor Type:</strong> ${data.prediction}</p>
            <p><strong>Confidence:</strong> ${data.confidence}%</p>
        `;

    } catch (error) {
        clearTimeout(timeoutId);
        console.error(error);

        if (error.name === 'AbortError') {
            resultBox.innerHTML = `
                Request timed out after 3 minutes. 
                The server may be overwhelmed — please try again.
            `;
        } else {
            resultBox.innerHTML = `
                Woops looks like I failed to analyze the image.
                Tell me did u post something way beyond my potential
            `;
        }
    }
}