# Cron expression : (minute), (hour), (day of month), (month), (day of week)
# Using Unix Cron Generator : https://crontab-generator.org/

from django_q.models import Schedule


class scheduler:
    def register(self):
        return {
            # "app.Jobs.ExampleJob.ExampleJob.handle": {"cron": "*/10 * * * *", "name": "Example schedule job"},
        }

    def handle(self):
        registerTasks = self.register()
        for func, value in registerTasks.items():
            schedule = Schedule.objects.filter(func=func).first()
            if schedule is None:
                self.createSchedule(func, value)
                continue

            if schedule.cron == value["cron"] and schedule.name == value["name"]:
                continue

            self.updateSchedule(func, value)

    def createSchedule(self, func, value):
        Schedule.objects.create(
            func=func,
            schedule_type=Schedule.CRON,
            cron=value["cron"],
            name=value["name"],
            repeats=-1,
        )

    def updateSchedule(self, func, value):
        params = {
            "cron": value["cron"],
            "name": value["name"],
            "repeats": -1,
        }
        Schedule.objects.filter(func=func).update(**params)
