class QueueGroupEnum:
    IMPORT = "import"
    EXPORT = "export"
    SEND_MAIL = "send_mail"
    UPLOAD_FILE = "upload_file"
    DELETE_FILE = "delete_file"
    SYNC_BANNER_FILEABLE = "SYNC_BANNER_FILEABLE"

    def all(self):
        return [
            self.IMPORT,
            self.EXPORT,
            self.SEND_MAIL,
            self.UPLOAD_FILE,
            self.DELETE_FILE,
            self.SYNC_BANNER_FILEABLE,
        ]
