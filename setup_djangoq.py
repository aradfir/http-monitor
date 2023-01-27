from django_q.models import Schedule

Schedule.objects.all().delete()
Schedule.objects.create(
    func='monitoring.tasks.check_urls',
    minutes=1,
    repeats=-1,
    schedule_type=Schedule.MINUTES,
    cluster='heartbeat',
)
