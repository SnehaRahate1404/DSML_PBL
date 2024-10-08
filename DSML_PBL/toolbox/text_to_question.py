import nltk
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk import RegexpParser
from nltk import ne_chunk
from nltk import DependencyGraph

def generate_question(input_text):
    # Tokenize input
    tokens = word_tokenize(input_text)

    # Part-of-speech tagging
    tagged_tokens = pos_tag(tokens)

    # Named Entity Recognition
    entities = ne_chunk(tagged_tokens)

    # Dependency Parsing
    parser = RegexpParser("NP: {<DT>?<JJ>*<NN>}")
    parsed_tree = parser.parse(tagged_tokens)

    # Semantic Role Labeling
    roles = DependencyGraph(parsed_tree)

    # Question Templates
    question_templates = {
        "What is {entity}?",
        "Where is {entity}?",
        "When did {entity} happen?",
        "Why did {entity} happen?"
    }

    # Generate questions
    questions = []
    for entity in entities:
        for role in roles:
            if entity.label() == role.label():
                question = question_templates[0].format(entity=entity[0])
                questions.append(question)

    return questions

input_text = "The quick brown fox jumps over the lazy dog."
questions = generate_question(input_text)
print(questions)
