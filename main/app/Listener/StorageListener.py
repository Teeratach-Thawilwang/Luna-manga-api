from app.Enums.QueueGroupEnum import QueueGroupEnum
from django_q.tasks import async_task


class StorageListener:
    def upload(self, file, uploadFile, collection):
        options = {
            "task_name": f"upload file {file.id}",
            "group": QueueGroupEnum.UPLOAD_FILE,
        }
        async_task("app.Jobs.StorageJob.StorageJob.upload", file, uploadFile, collection, q_options=options)

    def delete(self, file):
        options = {
            "task_name": f"delete file {file.id}",
            "group": QueueGroupEnum.DELETE_FILE,
        }
        async_task("app.Jobs.StorageJob.StorageJob.delete", file, q_options=options)
