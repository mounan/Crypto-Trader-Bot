from google.cloud import language_v1
from time import time
from time import sleep
import emoji
import yaml
import re
from google.oauth2 import service_account

def process_yaml(path):
    with open(path) as file:
        return yaml.safe_load(file)
    
def dump_json(json_file):
    import json
    print(json.dumps(json_file, indent=2, sort_keys=True))

def clean_text(text):
    '''
    remove urls & newlines, replace emojis to texts, remove @someone
    
    '''
    url_pattern = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
    at_pattern = r'@[A-Za-z0-9_-]*'
    text = re.sub(url_pattern, '', text, flags=re.S).replace('\n', ' ').replace('&amp;', 'and')
    text = re.sub(at_pattern, '', text, flags=re.S)
    text = emoji.demojize(text)
    return text

def contains_either(text, keywords):
    if len(keywords) == 0: return True
    for k in keywords:
        if k.lower() in text.lower():
            return True
    return False

def pprint_dict(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key) + ':')
        if isinstance(value, dict):
             pprint_dict(value, indent+1)
        else:
             print('\t' * (indent+1) + str(value))

def analyze_sentiment(text_content):
    """
    Analyzing Sentiment in a String

    Args:
      text_content The text content to analyze
    """

    google_credentials = service_account.Credentials.from_service_account_file("/Users/zmn/Downloads/sturdy-gamma-314101-8c7e836e8c75.json")
    client = language_v1.LanguageServiceClient(credentials=google_credentials)


    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    # Get overall sentiment of the input document
    print(u"Document sentiment score: {}".format(response.document_sentiment.score))
    print(
        u"Document sentiment magnitude: {}".format(
            response.document_sentiment.magnitude
        )
    )
    # Get sentiment for all sentences in the document
    for sentence in response.sentences:
        print(u"Sentence text: {}".format(sentence.text.content))
        print(u"Sentence sentiment score: {}".format(sentence.sentiment.score))
        print(u"Sentence sentiment magnitude: {}".format(sentence.sentiment.magnitude))

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
#     print(u"Language of the text: {}".format(response.language))


def analyze_entity_sentiment(text_content):
    """
    Analyzing Entity Sentiment in a String

    Args:
      text_content The text content to analyze
    """

    google_credentials = service_account.Credentials.from_service_account_file("/Users/zmn/Downloads/sturdy-gamma-314101-8c7e836e8c75.json")
    client = language_v1.LanguageServiceClient(credentials=google_credentials)


    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = language_v1.EncodingType.UTF8

    response = client.analyze_entity_sentiment(request = {'document': document, 'encoding_type': encoding_type})
    # Loop through entitites returned from the API
    for entity in response.entities:
        print('#'*30)
        print(u"Representative name for the entity: {}".format(entity.name))
        # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
        print(u"Entity type: {}".format(language_v1.Entity.Type(entity.type_).name))
        # Get the salience score associated with the entity in the [0, 1.0] range
        print(u"Salience score: {}".format(entity.salience))
        # Get the aggregate sentiment expressed for this entity in the provided document.
        sentiment = entity.sentiment
        print(u"Entity sentiment score: {}".format(sentiment.score))
        print(u"Entity sentiment magnitude: {}".format(sentiment.magnitude))
        # Loop over the metadata associated with entity. For many known entities,
        # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
        # Some entity types may have additional metadata, e.g. ADDRESS entities
        # may have metadata for the address street_name, postal_code, et al.
        for metadata_name, metadata_value in entity.metadata.items():
            print(u"{} = {}".format(metadata_name, metadata_value))

        # Loop over the mentions of this entity in the input document.
        # The API currently supports proper noun mentions.
#         for mention in entity.mentions:
#             print(u"Mention text: {}".format(mention.text.content))
#             # Get the mention type, e.g. PROPER for proper noun
#             print(
#                 u"Mention type: {}".format(language_v1.EntityMention.Type(mention.type_).name)
#             )

    # Get the language of the text, which will be the same as
    # the language specified in the request or, if not specified,
    # the automatically-detected language.
#     print(u"Language of the text: {}".format(response.language))
