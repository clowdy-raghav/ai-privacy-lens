const button = document.getElementById("analyzeButton");
const result = document.getElementById("result");

button.addEventListener("click", async function(){
    result.textContent = "Analyzing...";

    const response = await fetch("/analyze");

    const data = await response.json();

    result.textContent = "Conversations: " + data.conversations + " | Messages: " + data.messages;
});