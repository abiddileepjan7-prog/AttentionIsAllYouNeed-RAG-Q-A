const form = document.getElementById("question-form");
const questionInput = document.getElementById("question");
const answerBox = document.getElementById("answer");
const submitButton = document.getElementById("submit-button");
const statusPill = document.getElementById("status-pill");

function setStatus(state, text) {
    statusPill.className = `status ${state}`;
    statusPill.textContent = text;
}

questionInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        form.requestSubmit();
    }
});

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const question = questionInput.value.trim();
    if (!question) {
        answerBox.textContent = "Please enter a question before submitting.";
        setStatus("error", "Empty");
        return;
    }

    submitButton.disabled = true;
    setStatus("loading", "Thinking");
    answerBox.textContent = "Retrieving context and generating an answer...";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ question }),
        });

        if (!response.ok) {
            throw new Error(`Request failed with status ${response.status}`);
        }

        const data = await response.json();
        answerBox.textContent = data.answer || "No answer was returned by the backend.";
        setStatus("success", "Answered");
    } catch (error) {
        answerBox.textContent =
            "The frontend could not reach the backend or the model request failed. Check the server logs and confirm your API key is set.";
        setStatus("error", "Error");
        console.error(error);
    } finally {
        submitButton.disabled = false;
    }
});
