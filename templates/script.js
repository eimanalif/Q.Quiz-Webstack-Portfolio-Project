document.addEventListener('DOMContentLoaded', () => {
    fetchQuizzes();
});

function fetchQuizzes() {
    fetch('/get_quizzes')
        .then(response => response.json())
        .then(data => {
            if (data.length === 0) return;
            const quiz = data[0];
            renderQuiz(quiz);
        })
        .catch(error => {
            console.error('Error fetching quizzes:', error);
        });
}

function renderQuiz(quiz) {
    const quizContainer = document.getElementById('quiz-container');
    quizContainer.innerHTML = '';
    
    quiz.questions.forEach((question, index) => {
        const questionDiv = document.createElement('div');
        questionDiv.classList.add('question');
        questionDiv.innerHTML = `
            <p>${index + 1}: ${question.text}</p>
            <ul class="answers">
                ${question.options.map(option => `
                    <li>
                        <input type="radio" id="q${question.id}_${option.id}" name="q${question.id}" value="${option.id}" required>
                        <label for="q${question.id}_${option.id}">${option.text}</label>
                    </li>
                `).join('')}
            </ul>
        `;
        quizContainer.appendChild(questionDiv);
    });
}

function evaluateQuiz() {
    const userAnswers = document.querySelectorAll('input[type="radio"]:checked');
    let score = 0;

    questions.forEach((question, index) => {
        const userAnswer = userAnswers[index].value;
        if (userAnswer === question.correctAnswer) {
            score++;
        }
    });

    // Display the score or redirect to a results page
    alert(`You scored ${score} out of ${questions.length}`);
}
