
# Importing Libraries:
# The script begins by importing two libraries: `spacy` for natural language processing and `random` for generating random choices.

import spacy
import random

# Load English language model
# It loads the English language model for spaCy named "en_core_web_sm" using `spacy.load("en_core_web_sm")`. This model is used for processing and analyzing the text.

nlp = spacy.load("en_core_web_sm")

# get_mca_questions` Function:
# A function named `get_mca_questions` is defined, which takes two arguments: `context` (the text from which questions will be generated) and `num_questions` (the number of questions to be generated).

def get_mca_questions(context: str, num_questions: int):
    doc = nlp(context)

    def generate_mcq_with_multiple_correct(question, correct_answers, other_options, num_options=4):
        options = correct_answers + other_options
        random.shuffle(options)

        mcq = {
            "question": question,
            "options": options,
            "correct_answers": correct_answers
        }

        return mcq

# generate_mcq_with_multiple_correct` Function:
# A nested function named `generate_mcq_with_multiple_correct` is defined within `get_mca_questions`. This function is responsible for generating a single MCQ with multiple correct answers.
# It takes a `question` (the question text), `correct_answers` (a list of correct answer options), `other_options` (a list of incorrect answer options), and an optional argument `num_options` (the number of answer options, which is set to 4 by default).

    def generate_variety_question():
        sentence = random.choice(list(doc.sents))
        blank_word = random.choice([token for token in sentence if not token.is_punct])

        question_text = sentence.text.replace(blank_word.text, "______")
        correct_answers = [blank_word.text]

        other_options = [token.text for token in doc if token.is_alpha and token.text != correct_answers[0]]
        num_correct_options = random.randint(1, 2)  # Generate 1 or 2 correct options
        correct_answers.extend(random.sample(other_options, num_correct_options))

        num_other_options = min(4 - num_correct_options, len(other_options))
        other_options = random.sample(other_options, num_other_options)

        mcq = generate_mcq_with_multiple_correct(question_text, correct_answers, other_options)
        return mcq

    questions = [generate_variety_question() for _ in range(num_questions)]

#`Generate_variety_question` Function:
# Another nested function named `generate_variety_question` is defined within `get_mca_questions`. This function generates a variety of MCQs with blank spaces in random sentences of the given context.
# It selects a random sentence from `doc` and a random non-punctuation token within that sentence.
# It replaces the selected token with "______" to create a question with a blank space.
# It generates one or two correct answer options and selects other random options from the text.

    mca_questions = []
    for i, question in enumerate(questions, start=1):
        question_str = f"Q{i}: {question['question']}\n"
        options_str = ""
        for j, option in enumerate(question['options']):
            options_str += f"{j+1}. {option}\n"

        correct_options_formatted = " & ".join([f"({chr(97+question['options'].index(ans))})" for ans in question['correct_answers']])
        correct_options_str = f"Correct Options: {correct_options_formatted}"

        mca_question = f"{question_str}{options_str}{correct_options_str}\n"
        mca_questions.append(mca_question)

    return mca_questions


# Printing MCQs:
# Finally, the script prints the generated MCQs, displaying each question along with answer options and the correct answer options.

context = input("Enter the paragraph: ")
num_questions = int(input("Enter the number of questions: "))
mca_questions = get_mca_questions(context, num_questions)
for question in mca_questions:
    print(question)

# The code essentially allows you to input a paragraph, and it generates multiple-choice questions based on that paragraph with blank spaces. The answer options are also randomly selected from the text, providing a variety of MCQs for practice or assessment.
