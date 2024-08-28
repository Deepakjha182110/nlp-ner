import spacy


def main():
    # Load the best model
    nlp = spacy.load("C:/Users/dkjha/PycharmProjects/nlp-ner-poc/customer/output/model-best")

    # Use the model to predict entities in a new text
    doc = nlp("Hello Shanvi, how are you doing. Are you coming today, Can you pls connect with me here: awsds@erjekrej.com")

    # Print the detected entities
    for ent in doc.ents:
        print(ent.text, ent.label_)


if __name__ == '__main__':
    main()
