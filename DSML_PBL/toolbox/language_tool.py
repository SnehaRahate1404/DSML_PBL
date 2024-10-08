# import language_tool_python

# # Initialize the LanguageTool instance for English
# tool = language_tool_python.LanguageTool('en-US')

# # The sentence to check
# sentence = "This are an example of a bad sentence."

# # Check the sentence
# matches = tool.check(sentence)

# # Print the matches
# for match in matches:
#     print(f"Error: {match.ruleId}")
#     print(f"Message: {match.message}")
#     print(f"Incorrect: {sentence[match.offset:match.offset + match.errorLength]}")
#     print(f"Suggestions: {', '.join(match.replacements)}")
#     print()


# # Optionally, you can also auto-correct the sentence
# corrected_sentence = language_tool_python.utils.correct(sentence, matches)
# print(f"Corrected Sentence: {corrected_sentence}")

import language_tool_python

# Initialize the LanguageTool instance for English
tool = language_tool_python.LanguageTool('en-US')

# Function to check and print grammatical errors in a sentence
def check_sentence(sentence):
    matches = tool.check(sentence)
    for match in matches:
        print(f"Error: {match.ruleId}")
        print(f"Message: {match.message}")
        print(f"Incorrect: {sentence[match.offset:match.offset + match.errorLength]}")
        print(f"Suggestions: {', '.join(match.replacements)}")
        print()
    corrected_sentence = language_tool_python.utils.correct(sentence, matches)
    return corrected_sentence, len(matches) == 0

# Function to calculate the percentage of correct sentences in the text
def check_text_accuracy(text):
    sentences = text.split('.')
    total_sentences = len(sentences)
    correct_sentences = 0

    for sentence in sentences:
        if sentence.strip():  # Check if the sentence is not empty
            corrected_sentence, is_correct = check_sentence(sentence)
            if is_correct:
                correct_sentences += 1
            print(f"Original Sentence: {sentence}")
            print(f"Corrected Sentence: {corrected_sentence}")
            print()

    if total_sentences == 0:
        return 0.0  # Avoid division by zero

    accuracy = (correct_sentences / total_sentences) * 100
    return accuracy

# Example text
# text = "he are not doing well.But he is trying for it."
text="Hi how are you today I am not feeling well"

# Check text accuracy
accuracy = check_text_accuracy(text)
print(f"Percentage of correct sentences: {accuracy:.2f}%")
