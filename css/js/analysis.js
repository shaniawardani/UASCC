document.getElementById("predictionForm").addEventListener("submit", async function (e) {
    e.preventDefault();

    const tahun = document.getElementById("tahun").value;
    const kecamatan = document.getElementById("kecamatan").value;
    const target = document.getElementById("target").value;

    const formData = { tahun: tahun, kecamatan: kecamatan, target: target };

    // Reset result text for new submission
    document.getElementById("resultText").innerText = "Memproses prediksi...";
    document.getElementById("predictionResult").style.display = "block";

    try {
        const response = await fetch("http://localhost:5000/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(formData),
        });

        const result = await response.json();

        if (result.error) {
            document.getElementById("resultText").innerText = `Error: ${result.error}`;
        } else {
            document.getElementById("resultText").innerText = `Hasil Prediksi: ${result.prediction}`;
        }
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("resultText").innerText = "Terjadi kesalahan. Mohon coba lagi.";
    }
});
