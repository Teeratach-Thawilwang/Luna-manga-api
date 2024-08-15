from sys import modules

from django_q.tasks import async_task

from app.Enums.QueueGroupEnum import QueueGroupEnum


class StorageListener:
    def upload(self, file, uploadFile, collection, isSync):
        if not isSync:
            options = {
                "task_name": f"upload file {file.id}",
                "group": QueueGroupEnum.UPLOAD_FILE,
            }
            print("use queue")
            async_task("app.Jobs.StorageJob.StorageJob.upload", file, uploadFile, collection, q_options=options)
        else:
            if "StorageJob" not in modules:
                from app.Jobs.StorageJob import StorageJob

            print("use sync")
            StorageJob.upload(file, uploadFile, collection)

    def delete(self, file):
        options = {
            "task_name": f"delete file {file.id}",
            "group": QueueGroupEnum.DELETE_FILE,
        }
        async_task("app.Jobs.StorageJob.StorageJob.delete", file, q_options=options)
