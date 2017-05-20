from InformationRetrieval import *


username = "f97b81ce-7cab-4cfc-889a-efd669f9fd92"
password = "7fj1TNByAYqx"

# Create InformationRetrieval instance to handle analysis
retrieval = InformationRetrieval(username=username,
                                 password=password)

# Add the list of wanted features
retrieval.add_features_and_weights(['keywords', 'concepts', 'entities'], [1, 1, 1])

# # Add a test query
retrieval.add_source("How has immigration affected the United States economy", SourceType.query)
retrieval.add_source("What crimes have immigrants commited in America", SourceType.query)
# retrieval.add_source("Gambling should be outlawed for people under 18", SourceType.query)
# retrieval.add_source("The existence of God is undeniable.", SourceType.query)
# retrieval.add_source("God God God God Existence of God God Existence", SourceType.query)
# retrieval.add_source("Gun laws are too strict in America", SourceType.query)
# retrieval.add_source("Dogs are a great pet especially for Veterans", SourceType.query)
# retrieval.add_source("Cats are not good pets for little kids", SourceType.query)
# retrieval.add_source("Taxes in the United States should be lowered", SourceType.query)
# retrieval.add_source("Taxes in Mexico should be lowered", SourceType.query)
#
# # Add a test document
# retrieval.add_source("http://gun-control.procon.org", SourceType.document)
# retrieval.add_source("https://en.wikipedia.org/wiki/African-American_Civil_Rights_Movement_(1954–1968)",
#                      SourceType.document)
# retrieval.add_source("https://en.wikipedia.org/wiki/Dog", SourceType.document)
# retrieval.add_source("https://en.wikipedia.org/wiki/Martin_Luther_King_Jr.", SourceType.document)
# retrieval.add_source("https://www.washingtonpost.com/business/economy/washington-braces-for-details-of-trumps-tax-reform-plan/2017/04/25/1fba8b30-29df-11e7-a616-d7c8a68c1a66_story.html?utm_term=.edfd96806ae5", SourceType.document)
# retrieval.add_source("https://americansfortaxfairness.org/tax-fairness-briefing-booklet/fact-sheet-taxing-wealthy-americans/", SourceType.document)
# retrieval.add_source("http://www.worldwide-tax.com/mexico/mexico_taxes.asp", SourceType.document)
#
# retrieval.score_sources()
#
# retrieval.display_scores()

# print(retrieval.queries[0].analysis['categories'])
# print(retrieval.documents[0].analysis['categories'])
#
#
# print(retrieval.queries[0].analysis['keywords'])
# print(retrieval.documents[0].analysis['keywords'])

# file_gambling = open("Gambling", "r+")
# gambling = file_gambling.read()
#
# file_god = open("God", "r+")
# god = file_god.read()
#
# file_guns = open("Gun_control2", "r+")
# guns = file_guns.read()

file_immigration = open("Immigration", "r+")
immigration = file_immigration.read()

file_immigration_and_crime = open("Immigration_and_crime", "r+")
immigration_and_crime = file_immigration_and_crime.read()

# file_god = open("sentences/Existence_of_God", "r+", encoding="utf-8")
# file_gambling = open("sentences/Gambling", "r+", encoding="utf-8")
#
# god = file_god.read()
# gambling = file_gambling.read()


#
# retrieval.add_source(gambling, SourceType.document)
# retrieval.add_source(guns, SourceType.document)
# retrieval.add_source(gambling, SourceType.document)
# retrieval.add_source(god, SourceType.document)
retrieval.add_source(immigration, SourceType.document)
retrieval.add_source(immigration_and_crime, SourceType.document)

# for passage in retrieval.documents[0].passages:
#     print(passage.text)


sentences = retrieval.get_summary(n_docs=2, n_passages=2, n_sentences=7)

for query_index, query in enumerate(retrieval.queries):
    print("Query: ", query.text)
    for sentence in sentences[query_index]:
        print("\tText:", sentence.text)
        print("\tDocument ID: %i, Passage ID: %i, Sentence ID: %i" % (sentence.document_id, sentence.passage_id,
              sentence.sentence_id))
        print("\t\tScore:", sentence.scores[query_index].weighted_score(), "\n\n")


