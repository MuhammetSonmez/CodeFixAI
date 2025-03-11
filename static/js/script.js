document
  .getElementById("debug-form")
  .addEventListener("submit", async function (event) {
    event.preventDefault();
    const fileInput = document.getElementById("file-input").files[0];
    const errorMessage = document.getElementById("error-message");
    const debugButton = document.getElementById("debug-button");
    const loader = document.getElementById("loader");

    if (!fileInput) {
      errorMessage.style.display = "block";
      return;
    } else {
      errorMessage.style.display = "none";
    }

    loader.style.display = "inline-block";
    debugButton.disabled = true;

    const reader = new FileReader();
    reader.onload = function (e) {
      document.getElementById("original-code").textContent =
        e.target.result;
      hljs.highlightElement(document.getElementById("original-code"));
      document.getElementById("original-code-container").style.display =
        "block";
    };
    reader.readAsText(fileInput);

    const formData = new FormData();
    formData.append("file", fileInput);

    try {
      const response = await fetch("/debug", {
        method: "POST",
        body: formData,
      });

      const result = await response.json();
      const outputContainer = document.getElementById("fixed-code-container");
      const outputElement = document.getElementById("output");
      const downloadLink = document.getElementById("download-link");

      if (response.ok) {
        outputElement.textContent = result.fixed_code;
        hljs.highlightElement(outputElement);
        outputContainer.style.display = "block";
        downloadLink.href = result.download;
        downloadLink.style.display = "block";
        downloadLink.innerText = "Download Fixed Code";
      } else {
        outputElement.textContent = "Error: " + result.detail;
        outputContainer.style.display = "block";
      }
    } catch (error) {
      console.error("Debugging failed:", error);
    } finally {
      loader.style.display = "none";
      debugButton.disabled = false;
    }
  });
