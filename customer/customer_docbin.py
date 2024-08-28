import spacy
from spacy.tokens import DocBin
import random
import os
import warnings

from Random_text_generation import generate_text
from customer.oracle_util import OracleDB

training_data_path = "C:/Users/dkjha/PycharmProjects/nlp-ner-poc/customer/customer_data.spacy"
dev_validation_path = "C:/Users/dkjha/PycharmProjects/nlp-ner-poc/customer/validation_data.spacy"


def convert_to_spacy_format(lang, data, output_path):
    # create blank Language class
    nlp = spacy.blank(lang)
    doc_bin = DocBin()

    for text, annotations in data:
        doc = nlp.make_doc(text)
        ents_ = []
        for start, end, label in annotations["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is None:
                msg = f"Skipping entity [{start}, {end}, {label}] in the following text because the character span '{doc.text[start:end]}' does not align with token boundaries:\n\n{repr(text)}\n"
                warnings.warn(msg)
            else:
                ents_.append(span)
        doc.ents = ents_
        doc_bin.add(doc)
    doc_bin.to_disk(output_path)


def remove_file(file_path):
    # Check if the file exists
    if os.path.exists(file_path):
        # Remove the file
        os.remove(file_path)
        print(f"{file_path} has been removed.")
    else:
        print(f"{file_path} does not exist.")


def main():
    # Fetch all data from Oracle Customer Table
    db = OracleDB.create_instance()
    rows = db.execute_select("SELECT (firstname || ' ' || lastname), phone1, email FROM CUSTOMER WHERE phone1 is not null AND NOT REGEXP_LIKE(phone1, '[a-zA-Z]') AND NOT REGEXP_LIKE(phone1, '\.') AND NOT REGEXP_LIKE(phone1, '^-') AND rownum <600")
    # Annotate all rows
    data_list = generate_text(rows)
    print("data size : ", len(data_list))
    random.shuffle(data_list)

    # Split data: 70% training, 20% validation
    split_point = int(len(data_list) * 0.7)
    train_data = data_list[:split_point]
    validation_data = data_list[split_point:]

    remove_file(training_data_path)
    # Convert training data
    convert_to_spacy_format("en", train_data, training_data_path)

    remove_file(dev_validation_path)
    # Convert validation data
    convert_to_spacy_format("en", validation_data, dev_validation_path)


if __name__ == '__main__':
    main()
