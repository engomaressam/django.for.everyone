from django.http import HttpResponse

def index(request):
    # session counter
    count = request.session.get('count', 0) + 1
    request.session['count'] = count

    # build response and set cookie
    resp = HttpResponse(f"Hello from hello. 296a4a44 (visits: {count})")
    resp.set_cookie('dj4e_cookie', '296a4a44', max_age=1000)
    return resp
