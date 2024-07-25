from app.Providers.StorageManager import StorageManager


class StorageJob:
    def upload(file, uploadFile, collection):
        StorageManager(file).upload(uploadFile, collection)

    def delete(file):
        StorageManager(file).delete()
