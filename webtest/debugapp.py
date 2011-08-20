from webob import Request, Response
try:
    sorted
except NameError:
    from webtest import sorted

__all__ = ['debug_app']

def debug_app(environ, start_response):
    req = Request(environ)
    if req.path_info == '/form.html' and req.method == 'GET':
        resp = Response(content_type='text/html')
        resp.body = '''<html><body>
        <form action="/form-submit" method="POST">
            <input type="text" name="name">
            <input type="submit" name="submit" value="Submit!">
        </form></body></html>'''
        return resp(environ, start_response)

    if 'error' in req.GET:
        raise Exception('Exception requested')
    status = str(req.GET.get('status', '200 OK'))

    parts = []
    for name, value in sorted(environ.items()):
        if name.upper() != name:
            value = repr(value)
        parts.append('%s: %s\n' % (name, value))

    if req.content_length:
        req_body = req.body
    else:
        req_body = ''
    if req_body:
        parts.append('-- Body ----------\n')
        parts.append(req_body)
    body = ''.join(parts)

    if status[:3] in ('204', '304') and not req_body:
        body = ''

    headers = [
        ('Content-Type', 'text/plain'),
        ('Content-Length', str(len(body)))]

    for name, value in req.GET.items():
        if name.startswith('header-'):
            header_name = name[len('header-'):]
            headers.append((header_name, value))

    start_response(status, headers)
    if req.method == 'HEAD':
        return ['']
    return [body]

def make_debug_app(global_conf):
    """
    An application that displays the request environment, and does
    nothing else (useful for debugging and test purposes).
    """
    return debug_app
