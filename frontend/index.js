const button = document.getElementById("analyzeButton");
const result = document.getElementById("result");

button.addEventListener("click", async function(){
    result.textContent = "Analyzing...";

    const response = await fetch("/analyze");
    const data = await response.json();

    let html = "";

    html += "<h2>Privacy Analysis</h2>";

    html += `
        <div>
            <strong> Conversations:</strong> ${data.conversations}
            &nbsp; | &nbsp;
            <strong>Messages:</strong> ${data.messages}
            &nbsp; | &nbsp;
            <strong>Findings:</strong> ${data.summary.total_findings}
        </div>`;

        html += "<h3>Privacy Categories</h3>";

        for (const category in data.summary.categories){
            html += `
            <p>
                <strong>${category}</strong>:
                ${data.summary.categories[category]}
            </p>`;
        }

        html += "<h3>Detected Information</h3>";

        for(const finding of data.findings){
            html += `
                <div>
                    <strong>${finding.type}</strong>
                    ${finding.value}
                    <br>
                    <small>
                        ${finding.category} | 
                        ${finding.conversation}
                    </small>
                    <p>${finding.evidence}</p>
                </div>
                <hr>`;
        }

        html += "<h3>Recurring Information</h3>";

        for(const item of data.recurrence){
            html += `
                <div>
                    <strong>${item.value}</strong>
                    <br>
                    Type: ${item.type}
                    <br>
                    Appeared in ${item.conversation_count} conversation(s)
                </div>
                <hr>`;
        }

    result.innerHTML = html;
});