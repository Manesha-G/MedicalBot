
document.addEventListener("DOMContentLoaded", function () {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const voiceBtn = document.getElementById("voice-btn");

    let stage = 1;
    let lastDiseases = null;
    let lastSpecialist = null;

    appendMessage("🤖 Hi, how can I help you?");
    appendMessage("💬 What symptoms are you experiencing?");

    function appendMessage(message, isBot = true) {
        const msgDiv = document.createElement("div");
        msgDiv.innerText = message;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;

        speak(message);
    }

    function speak(text) {
        const synth = window.speechSynthesis;
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = "en-US";
        utterance.rate = 1;
        utterance.pitch = 1;
        synth.speak(utterance);
    }

    function handleUserInput(input) {
        const userMessage = input.trim();
        if (!userMessage) return;

        appendMessage("👤 You: " + userMessage, false);
        userInput.value = "";

        if (stage === 1) {
            fetch("http://127.0.0.1:5000/predict", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ symptoms: userMessage })
            })
                .then(res => res.json())
                .then(data => {
                    if (data.error) {
                        appendMessage("⚠ " + data.error);
                        return;
                    }

                    lastDiseases = data.diseases;
                    lastSpecialist = data.specialist;

                    const diseaseMsg = data.diseases.map(d => `${d.name} (${d.confidence})`).join(", ");
                    appendMessage("✅ I’ve analyzed the symptoms.");
                    appendMessage(`🧾 Possible Disease(s): ${diseaseMsg}`);
                    appendMessage("💬 Would you like to know the recommended specialist? (yes/no)");
                    stage = 2;
                })
                .catch(err => {
                    console.error(err);
                    appendMessage("❌ Error processing your request.");
                });
        } else if (stage === 2) {
            if (userMessage.toLowerCase().includes("yes")) {
                appendMessage(`🩺 Recommended Specialist: ${lastSpecialist}`);
                appendMessage("📍 Do you want to find nearby doctors based on your PIN code? (yes/no)");
                stage = 3;
            } else {
                appendMessage("✅ No problem. Take care!");
                resetChat();
            }
        } else if (stage === 3) {
            if (userMessage.toLowerCase().includes("yes")) {
                appendMessage("🔢 Please enter your PIN code:");
                stage = 4;
            } else {
                appendMessage("✅ Got it! Take care.");
                resetChat();
            }
        } else if (stage === 4) {
            const pincode = userMessage;
            appendMessage(`📍 Searching for doctors near PIN code ${pincode}...`);
            fetchNearbyDoctors(pincode, lastSpecialist);
            resetChat(3000); // Reset after few seconds
        }
    }

    
function fetchNearbyDoctors(pincode, specialist) {
    fetch("http://127.0.0.1:5000/find_hospitals", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ pincode, specialist })
    })
        .then(res => res.json())
        .then(data => {
            if (data.hospitals && data.hospitals.length > 0) {
                appendMessage("🏥 Nearby hospitals:");
                data.hospitals.forEach(place => {
                    appendMessage(`• ${place.name}, ${place.address}`);
                });
            } else {
                appendMessage("❌ No hospitals found near this location.");
            }
        })
        .catch(err => {
            console.error(err);
            appendMessage("❌ Failed to fetch nearby hospitals.");
        });
}



    function resetChat(delay = 2000) {
        setTimeout(() => {
            lastDiseases = null;
            lastSpecialist = null;
            stage = 1;
            appendMessage("🤖 Hi again! What symptoms are you experiencing?");
        }, delay);
    }

    function sendMessage() {
        handleUserInput(userInput.value);
    }

    function recordVoice() {
        if (!("SpeechRecognition" in window || "webkitSpeechRecognition" in window)) {
            appendMessage("❌ Speech recognition not supported.");
            return;
        }

        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = "en-US";
        recognition.start();

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            userInput.value = transcript;
            sendMessage();
        };

        recognition.onerror = function (event) {
            appendMessage("❌ Voice input failed. Try again.");
        };
    }

    sendBtn.addEventListener("click", sendMessage);
    voiceBtn.addEventListener("click", recordVoice);
});
