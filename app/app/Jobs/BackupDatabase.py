import subprocess

from app.Settings.path import STORAGE_DIR, env


class BackupDatabase:
    def handle():
        backupFilename = "backup.sql"
        # cron of mariadb container will dumb on 03.00 every 5 day
        # schedule will work on 05.00 every 5 day

        # Find file name that "backup.sql"
        # compress file with gzip and upload to s3 on folder database-backup/
