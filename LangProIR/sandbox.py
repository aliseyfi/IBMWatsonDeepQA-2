from InformationRetrieval import InformationRetrieval

un = ""
pw = ""

ir = InformationRetrieval(username=un, password=pw)

ir.add_features_and_weights(['keywords', 'concepts', 'entities'], [1, 1, 1])
ir.add_query("Nuclear weapons should be reduced in number.")
ir.add_dataset("folder/path")

sentences = ir.get_summary(n_docs=1, n_passages=5, n_sentences=5)

for query_index, query in enumerate(ir.queries):
    print("Query: ", query.text)
    for sentence in sentences[query_index]:
        print("\tText:", sentence.text)
        print("\t\tScore:", sentence.scores[query_index].weighted_score(), "\n\n")
