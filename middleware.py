#  coding: utf-8
import datetime
from models import  UsersOnLine

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

class Db_request(object):
    def process_response(self, request, response):
        rec = UsersOnLine()
        rec.ip = str(get_client_ip(request))
        rec.date = datetime.datetime.now()
        try:
            rec.user = request.user
            rec.save()
        except:
            rec.user = None
            rec.save()

        return response