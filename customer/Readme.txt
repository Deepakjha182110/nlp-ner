#Training spaCy Model
#Once you have your training data, you can use it to train a spaCy model.

#First, create a configuration file using:
python -m spacy init config config.cfg --lang en --pipeline ner

#Modify the configuration file to point to your training data, and then run the training:
python -m spacy train config.cfg --output ./output --paths.train ./customer_data.spacy --paths.dev ./validation_data.spacy

#This will generate a model in the ./output directory, which you can then use to predict entities like
#name, phone, and email from new text data.

#Debug config file using if any error related to configuration!!
python -m spacy debug config config.cfg
