from models import Choice



def calculate_score(results):
    score = 0
    for result in results:
        # Fetch the user's selected choice using the result's choice_id
        user_choice = Choice.query.get(result.choice_id)
        
        # Fetch the correct choice for the question using the question_id
        correct_choice = Choice.query.filter_by(question_id=result.question_id, is_correct=True).first()
        
        # Compare the text of the user's choice and the correct choice
        if user_choice and correct_choice and user_choice.text == correct_choice.text:
            score += 1  # Increment score if the answer is correct

    return score
