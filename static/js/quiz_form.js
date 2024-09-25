document.addEventListener("DOMContentLoaded", function() {
    const csrfToken = document.querySelector('input[name="csrf_token"]').value;

    // Add new question
    const addQuestionBtn = document.getElementById('add-question');
    addQuestionBtn.addEventListener('click', function(e) {
        e.preventDefault();
        addNewQuestion();
    });

    // Function to add a new question block
    function addNewQuestion() {
        const questionList = document.getElementById('questions-list');
        const questionIndex = questionList.children.length;

        const questionTemplate = `
            <div class="question-block" id="question-${questionIndex}">
                <input type="hidden" name="questions-${questionIndex}-csrf_token" value="${csrfToken}">
                <label>Question ${questionIndex + 1}:</label>
                <input type="text" name="questions-${questionIndex}-text" class="form-control" required>
                
                <div class="choices-list" id="choices-${questionIndex}">
                    <!-- Placeholder for choices -->
                </div>
                <button class="btn btn-secondary add-choice" data-question-index="${questionIndex}">Add Choice</button>
                <button class="btn btn-danger remove-question" data-question-index="${questionIndex}">Remove Question</button>
            </div>
        `;

        questionList.insertAdjacentHTML('beforeend', questionTemplate);

        // Add event listener for the newly added "Add Choice" button
        document.querySelector(`#question-${questionIndex} .add-choice`).addEventListener('click', function(e) {
            e.preventDefault();
            addNewChoice(questionIndex);
        });

        // Add event listener for the "Remove Question" button
        document.querySelector(`#question-${questionIndex} .remove-question`).addEventListener('click', function(e) {
            e.preventDefault();
            removeQuestion(questionIndex);
        });
    }

    // Function to add a new choice to a specific question
    function addNewChoice(questionIndex) {
        const choiceList = document.getElementById(`choices-${questionIndex}`);
        const choiceIndex = choiceList.children.length;

        const choiceTemplate = `
            <div class="choice-block" id="choice-${questionIndex}-${choiceIndex}">
                <input type="hidden" name="questions-${questionIndex}-choices-${choiceIndex}-csrf_token" value="${csrfToken}">
                <input type="text" name="questions-${questionIndex}-choices-${choiceIndex}-text" class="form-control" placeholder="Choice Text" required>
                <label for="questions-${questionIndex}-choices-${choiceIndex}-is_correct">Correct?</label>
                <input type="checkbox" name="questions-${questionIndex}-choices-${choiceIndex}-is_correct" class="form-check-input">
                <button class="btn btn-danger remove-choice" data-question-index="${questionIndex}" data-choice-index="${choiceIndex}">Remove Choice</button>
            </div>
        `;

        choiceList.insertAdjacentHTML('beforeend', choiceTemplate);

        // Add event listener for the "Remove Choice" button
        document.querySelector(`#choice-${questionIndex}-${choiceIndex} .remove-choice`).addEventListener('click', function(e) {
            e.preventDefault();
            removeChoice(questionIndex, choiceIndex);
        });
    }

    // Function to remove a specific question
    function removeQuestion(questionIndex) {
        const questionBlock = document.getElementById(`question-${questionIndex}`);
        if (questionBlock) {
            questionBlock.remove();
        }
    }

    // Function to remove a specific choice
    function removeChoice(questionIndex, choiceIndex) {
        const choiceBlock = document.getElementById(`choice-${questionIndex}-${choiceIndex}`);
        if (choiceBlock) {
            choiceBlock.remove();
        }
    }
});
