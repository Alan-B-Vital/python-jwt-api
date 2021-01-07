class Writer:
    def __init__(self, file_path, open_mode):
        self.file = open(file_path, open_mode)

    def write(self, text):
        self.file.write(text)
