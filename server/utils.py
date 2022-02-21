from datetime import datetime


def make_date(val):
    d = datetime.fromisoformat(val)
    return d.strftime('%b %d, %Y %I:%M %p').replace(' AM', 'am').replace(' PM', 'pm')


def get_ip_from_request(request):
    return request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
