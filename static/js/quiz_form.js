document.addEventListener("DOMContentLoaded", function() {
    const addQuestionBtn = document.getElementById('add-question');
    const questionList = document.getElementById('questions-list');
    const quizForm = document.querySelector('form');

    let questionIndex = 0;  // Track the number of questions added

    addQuestionBtn.addEventListener('click', function() {
        addNewQuestion();
    });

    function addNewQuestion() {
        const questionTemplate = `
            <div class="question-block" id="question-${questionIndex}">
                <label for="question-${questionIndex}-text">Question ${questionIndex + 1}:</label>
                <input type="text" name="questions-${questionIndex}-text" class="form-control" required>

                <div class="choices-list" id="choices-${questionIndex}">
                    <!-- Choices will be added here -->
                </div>
                <button type="button" class="btn btn-secondary add-choice" data-question-index="${questionIndex}">Add Choice</button>
                <button type="button" class="btn btn-danger delete-question" data-question-id="${questionIndex}">Delete Question</button>
            </div>
        `;

        questionList.insertAdjacentHTML('beforeend', questionTemplate);

        const addChoiceBtn = document.querySelector(`#question-${questionIndex} .add-choice`);
        const deleteQuestionBtn = document.querySelector(`#question-${questionIndex} .delete-question`);

        addChoiceBtn.addEventListener('click', function() {
            const qIndex = this.getAttribute('data-question-index');
            addNewChoice(qIndex);
        });

        deleteQuestionBtn.addEventListener('click', function() {
            const questionId = this.getAttribute('data-question-id');
            document.getElementById(`question-${questionId}`).remove();
        });

        questionIndex++;
    }

    function addNewChoice(questionIndex) {
        const choiceList = document.getElementById(`choices-${questionIndex}`);
        const choiceIndex = choiceList.children.length;

        const choiceTemplate = `
            <div class="choice-block" id="choice-${questionIndex}-${choiceIndex}">
                <label for="choice-${questionIndex}-${choiceIndex}-text">Choice ${choiceIndex + 1}:</label>
                <input type="text" name="questions-${questionIndex}-choices-${choiceIndex}-text" class="form-control" required>
                <label for="choice-${questionIndex}-${choiceIndex}-is_correct">Correct:</label>
                <input type="checkbox" name="questions-${questionIndex}-choices-${choiceIndex}-is_correct" class="form-check-input">
                <button type="button" class="btn btn-danger delete-choice" data-choice-id="choice-${questionIndex}-${choiceIndex}">Delete Choice</button>
            </div>
        `;

        choiceList.insertAdjacentHTML('beforeend', choiceTemplate);

        const deleteChoiceBtn = document.querySelector(`#choice-${questionIndex}-${choiceIndex} .delete-choice`);
        deleteChoiceBtn.addEventListener('click', function() {
            const choiceId = this.getAttribute('data-choice-id');
            document.getElementById(choiceId).remove();
        });
    }

    // Redirect after form submission
    quizForm.addEventListener('submit', function(event) {
        event.preventDefault();  // Prevent the default form submission
        const formData = new FormData(quizForm);

        fetch(quizForm.action, {
            method: 'POST',
            body: formData
        }).then(response => {
            if (response.ok) {
                // Redirect to the home page after successful submission
                window.location.href = "/";
            } else {
                alert('There was a problem submitting the form.');
            }
        }).catch(error => {
            console.error('Error:', error);
        });
    });
});
