import random
from tqdm import tqdm
from datetime import datetime

from customer.oracle_util import OracleDB

# Define various sentence parts
intro = ["Contact", "Reach out to", "For more information, you can reach", "Hey, this is", "name: "]
phone_conjunctions = ["at", "via", "through", "using", "contact me at", "phone: "]
email_conjunctions = ["or at", "or via", "or through", "or using", "or contact me at", "or email: "]
endings = ["for further assistance.", "regarding any inquiries.", "with any questions."]
data_to_insert = []
insert_query = """
INSERT INTO annotation_data(text, person, phone, email, person_annotation, phone_annotation, email_annotation, datetime) 
Values(:1, :2, :3, :4, :5, :6, :7, :8)
"""


def process(rows):
    training_dict = {}
    for row in rows:
        name = row[0]
        phone = row[1]
        email = row[2]

        # Randomly select sentence components
        intro_part = random.choice(intro)
        phone_conjunction = random.choice(phone_conjunctions)
        email_conjunction = random.choice(email_conjunctions)
        ending = random.choice(endings)

        # Randomly decide on the inclusion of each entity
        # entities = [name if random.random() > 0.5 else None,
        #            phone if random.random() > 0.5 else None,
        #            email if random.random() > 0.5 else None]
        entities = [name, phone, email]

        # Construct sentences based on entities
        text = f"{intro_part} "
        if entities[0]:
            text += f"{entities[0]} "
        if entities[1]:
            text += f"{phone_conjunction} {entities[1]} "
        if entities[2]:
            text += f"{email_conjunction} {entities[2]} "
        text += ending

        training_dict[text] = row
    return training_dict


def contains_no_alpha(s):
    return not any(char.isalpha() for char in s)


def annotate_data(text, row):
    entities = []
    name = None
    phone = None
    email = None
    name_annot = None
    phone_annot = None
    email_annot = None
    # Check and add PERSON entity if present
    if row[0] in text:
        name_annot = (text.find(row[0]), text.find(row[0]) + len(row[0]), "PERSON")
        entities.append(name_annot)
        name = row[0]
    # Check and add PHONE entity if present
    if row[1] in text and contains_no_alpha(row[1]):
        phone_annot = (text.find(row[1]), text.find(row[1]) + len(row[1]), "PHONE")
        entities.append(phone_annot)
        phone = row[1]

    # Check and add EMAIL entity if present
    if row[2] in text:
        email_annot = (text.find(row[2]), text.find(row[2]) + len(row[2]), "EMAIL")
        entities.append(email_annot)
        email = row[2]

    date_time = datetime.now()
    data_to_insert.append((text, name, phone, email, str(name_annot) if name_annot is not None else None, str(phone_annot) if phone_annot is not None else None, str(email_annot) if email_annot is not None else None, date_time))

    return text, {"entities": entities}


def generate_text(rows):
    print("Rows from DB: ", len(rows))
    data_list = []
    merged_dict = {}
    db = OracleDB.create_instance()
    db.execute_delete("delete from annotation_data")

    for _ in tqdm(range(1)):
        training_data_dict = process(rows)
        merged_dict.update(training_data_dict)

    print("Total Training data size: ", len(merged_dict))
    for text, row in merged_dict.items():
        data_list.append(annotate_data(text, row))

    db.execute_insert_many(insert_query, data_to_insert)
    print("data_list size : ", len(data_list))

    return data_list
