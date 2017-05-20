import watson_developer_cloud.natural_language_understanding.features.v1 as features


# Holds all relevant information about a feature
# - name: string name representation
# - element: Watson feature representation
# - weight: weight to use for feature when calculating score
class Feature:

    def __init__(self, name, weight):
        self.name = name
        self.element = Feature.map_feature(name)
        self.weight = weight

    # Maps the string name representation of a feature to the Watson feature representation
    # - returns None if feature does not map to anything
    @staticmethod
    def map_feature(name):
        feature_name_mappings = {'keywords': features.Keywords(),
                                 'entities': features.Entities(),
                                 'concepts': features.Concepts(),
                                 'categories': features.Categories(),
                                 'sentiment': features.Sentiment(),
                                 'emotion': features.Emotion()}
        if name in feature_name_mappings:
            return feature_name_mappings[name]
        else:
            print("Invalid feature name")
            return None
