import os


class Dataset:
    def __init__(self, dir_path):
        self.contents = Dataset.read_dataset(dir_path)

    @staticmethod
    def read_dataset(dir_path):
        contents = []

        if dir_path[-1] is not "/":
            dir_path += "/"

        for fn in os.listdir(dir_path):
            with open(dir_path + fn, "rt", encoding="latin-1") as f:
                contents.append(f.read())

        return contents

    def get_contents(self):
        return self.contents
