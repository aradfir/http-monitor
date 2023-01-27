import requests

from monitoring.models import HeartBeat, URL


# check all urls for heartbeat
def check_urls():
    urls = URL.objects.all()
    for url in urls:
        check_url(url)


def check_url(url):
    try:
        response = requests.get(url.url)
        status = response.status_code
    except:
        status = 500
    HeartBeat.objects.create(url=url, status=status)
    if status/400/100 != 2:
        url.error_count += 1
    else:
        url.error_count = 0
    url.save()
