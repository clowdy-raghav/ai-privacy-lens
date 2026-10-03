const uploadButton = document.getElementById("uploadButton");
const fileInput = document.getElementById("fileInput");
const uploadStatus = document.getElementById("uploadStatus");
const analyzeButton = document.getElementById("analyzeButton");
const result = document.getElementById("result");

uploadButton.addEventListener("click", async function(){
    const file = fileInput.files[0];

    if(!file){
        uploadStatus.textContent = "Please select a JSON file first.";
        return;
    }

    uploadStatus.textContent = "Importing conversations...";
    const formData = new FormData();
    formData.append("file", file);

    try{
        const response = await fetch("/upload", {
            method: "POST",
            body: formData
        });

        const data = await response.json();

        if (!response.ok){
            uploadStatus.textContent = data.error;
            return;
        }

        uploadStatus.textContent = "Imported " + data.conversations  + " conversations successfully.";
    } catch (error){
        uploadStatus.textContent = "Upload failed: " + error.message;
    }
});

analyzeButton.addEventListener("click", async function(){
    result.textContent = "Analyzing...";

    try{
        const response = await fetch("/analyze");
        const data = await response.json();

        if (!response.ok){
            result.innerHTML = "<p> Error: " + data.error + " </p>";
            return;
        }

        let html = "";

        html += `
        <h2>Privacy Profile</h2>
        <div class="profile-grid">
            <div class="profile-card">
                <strong>Identity</strong>
                <span>${data.profile.identity.length}</span>
            </div>
            
            <div class="profile-card">
                <strong>Contact</strong>
                <span>${data.profile.contact.length}</span>
            </div>

            <div class="profile-card">
                <strong>Location</strong>
                <span>${data.profile.location.length}</span>
            </div>

            <div class="profile-card">
                <strong>Education</strong>
                <span>${data.profile.education.length}</span>
            </div>
            
            <div class="profile-card">
            <strong>Other</strong>
            <span>${data.profile.other.length}</span>
        </div>

    </div>`;

    html += `<h2>Privay Summary</h2>`

    html += `
        <div class="finding-card">
        <p><strong>Total Conversations:</strong>${data.conversations}</p>
        <p><strong>Total Messages:</strong>${data.messages}</p>
        <p><strong>Detected Disclosures:</strong>${data.summary.total_findings}</p>
        <p><strong>High-confidence findings:</strong>"${data.summary.high_confidence}"</p>
        <p><strong>Potential Inferences:</strong>"${data.inferences.length}"</p>
    </div>`;

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

    for(let i = 0; i < data.findings.length; i++){
        const finding = data.findings[i];
        html += `
            <div class="finding-card">
                <div class="finding-header">
                    <strong>${finding.type}</strong>
                    <span class="severity-badge">${finding.severity || "medium"}</span>
                </div>
                <h4>${finding.value}</h4>
                <p><strong>Classification:</strong>${finding.classification || "explicit"}</p>
                <p><strong>Confidence:</strong>${finding.confidence || "unknown"}</p>
                <p><strong>Source:</strong>${finding.conversation}</p>
                <p><strong>Evidence:</strong>"${finding.evidence}"</p>
                <p><strong>Status:</strong><span class="finding-status" id="status-${i}">${finding.status || "review"}</span></p>
                <div class="finding-actions">
                    <button class="keep-button" data-index="${i}"> KEEP </button>
                    <button class="review-button" data-index="${i}"> REVIEW </button>
                    <button class="delete-button" data-index="${i}"> DELETE </button>
                </div>
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

    html += "<h3>Potential Inferences</h3>";

    if (data.inferences.length === 0){
        html += `
        <p>No potential cross-conversation inferences detected</p>`;
    }
    else{
        for (const inference of data.inferences){
            html += `
            <div>
                <strong>${inference.value}</strong>
                <br>
                Classification: ${inference.classification}
                <br>
                Confidence: ${inference.confidence}
                <p>${inference.explanation}</p>
                <strong>Evidence:</strong>`;
            
                for (const evidence of inference.evidence){
                    html += `<blockquote>${evidence}</blockquote>`;
                }

            html += `</div>
                    <hr>`;
        }
    }
    result.innerHTML = html;

    document.querySelectorAll(".keep-button").forEach(
        function(button){
            button.addEventListener("click", function(){
                updateFindingStatus(button, "keep");
            });
        }
    );
    document.querySelectorAll(".review-button").forEach(
        function(button){
            button.addEventListener("click", function(){
                updateFindingStatus(button, "review");
            });
        }
    );
    document.querySelectorAll(".delete-button").forEach(
        function(button){
            button.addEventListener("click", function(){
                updateFindingStatus(button, "delete");
            });
        }
    );
    function updateFindingStatus(button, status){
        console.log("updateFindingStatus was called");
    
        const card = button.closest(".finding-card");
    
        if (!card) {
            console.log("NO CARD");
            return;
        }
    
        const statusElement = card.querySelector(".finding-status");
    
        if (!statusElement) {
            console.log("NO STATUS ELEMENT");
            return;
        }
    
        console.log("FOUND STATUS ELEMENT:", statusElement);
    
        statusElement.textContent = status;
    
        if (status === "delete"){
            card.classList.add("deleted-finding");
        } else {
            card.classList.remove("deleted-finding");
        }
    }
    
 } catch(error){
        result.innerHTML = "<p>Error: " + error.message + "</p>";
    }
});