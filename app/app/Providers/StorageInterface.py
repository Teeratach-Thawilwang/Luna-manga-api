class StorageInterface:
    def __init__(self):
        pass

    def downloadToInMemory(self, sourcePath):
        pass

    def upload(self, sourcePath, destinationPath, contentType):
        pass

    def uploadInMemoryFile(self, file, destinationPath, contentType):
        pass

    def delete(self, sourcePath):
        pass
