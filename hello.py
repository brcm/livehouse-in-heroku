# coding=utf-8
import os
import sys
from wsgiref.simple_server import make_server
import urllib2
import codecs
import cookielib
reload(sys)   
sys.setdefaultencoding('utf-8')

def application(environ,start_response):

    sourceUrl = "https://livehouse.in"

    try:
        requestUrl = str(environ["PATH_INFO"])+"?"+str(environ["QUERY_STRING"])
        httpHost = str(environ["HTTP_HOST"])
        try:
            httpAccept = str(environ["HTTP_ACCEPT"])
        except:
            httpAccept = ""
        try:
            userAgent = str(environ["HTTP_USER_AGENT"])
        except:
            userAgent = ""
        try:
            httpCookie = str(environ["HTTP_COOKIE"])
        except:
            httpCookie = ""
        try:
            httpLang = str(environ["HTTP_ACCEPT_LANGUAGE"])
        except:
            httpLang = ""
        try:
            httpEncode = str(environ["HTTP_ACCEPT_ENCODING"])
        except:
            httpEncode = ""
        try:
            bodyLength = int(environ.get('CONTENT_LENGTH', '0'))
        except ValueError:
            bodyLength = 0
    except:
        requestUrl = ""

    # Local Javascript CDN
    if str(environ["PATH_INFO"]) == '/cdn-dat/js':
        f = codecs.open('js/' + str(environ["QUERY_STRING"]), 'r', 'utf-8')
        html = str(f.read())
        status = '200 OK'
        response_headers  =  [('Content-Type', 'text/javascript;charset=utf-8'),('Cache-Control', 'public, max-age=2592000'),('Content-Length', str(len(html)))]
        start_response(status, response_headers)
        return html
    
    # Advs block listener
    if str(environ["PATH_INFO"]) == '/cdn-dat/adb':
        html = ""
        status = '200 OK'
        response_headers  =  [('Content-Type', 'text/html;charset=utf-8'),('Cache-Control', 'public, max-age=2592000'),('Content-Length', str(len(html)))]
        start_response(status, response_headers)
        return html

    try:
        cookies = cookielib.LWPCookieJar()
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookies))
        opener.addheaders = [('User-Agent', userAgent)]
        opener.addheaders = [('Accept',httpAccept)]
        opener.addheaders = [('Accept-Encoding',httpEncode)]
        opener.addheaders = [('Accept-Language',httpLang)]
        opener.addheaders = [('Cookie',httpCookie)]
        opener.addheaders = [('Pragma','no-cache')]
        if bodyLength != 0:
            body = environ['wsgi.input'].read(bodyLength)
            html = opener.open(sourceUrl+requestUrl, body).read()
        else:
            html = opener.open(sourceUrl+requestUrl).read()
        
        # Do cookies process
        cs = ['%s=%s; expires=Thu, 01-Jan-1970 00:00:01 GMT; Max-Age=0; path=/; domain=%s' % (c.name, c.value, httpHost) for c in cookies]
        cookie = '; '.join(cs)   

        # Replace the blocked resource
        html = html.replace('https://ajax.googleapis.com/ajax/libs/jquery/','//cdn.bootcss.com/jquery/')
        html = html.replace('https://ajax.googleapis.com/ajax/libs/angularjs/','//cdn.bootcss.com/angular.js/')
        html = html.replace('https://cdn.firebase.com/js/client/1.1.2/firebase.js','/cdn-dat/js?firebase.js')
        html = html.replace(sourceUrl,'//' + httpHost)
        
        # Replace Flash Player
        html = html.replace('//static.cdn.livehouse.in/assets/GrindPlayer-4a087377ed.swf','//static.cdn.livehouse.in/assets/video-js-flashls-194ba172ae.swf')
        html = html.replace('grind','flashls')
        
        # Filter Advs Javascripts
        html = html.replace('//imasdk.googleapis.com/','/cdn-dat/adb?')
        html = html.replace('//pagead2.googlesyndication.com/','/cdn-dat/adb?')
        html = html.replace('//partner.googleadservices.com/','/cdn-dat/adb?')
        html = html.replace('//www.googletagservices.com/','/cdn-dat/adb?')
        html = html.replace('//www.google-analytics.com/','/cdn-dat/adb?')
        html = html.replace('https://connect.facebook.net/','/cdn-dat/adb?')
        html = html.replace('//connect.facebook.net/','/cdn-dat/adb?')
        
        # Convernt T/S Chinese
        html = html + '<script src="/cdn-dat/js?jquery.s2t.js" type="text/javascript"></script>'
        html = html + '<script type="text/javascript">$(\'body\').t2s();</script>'
    except:
        html = "Can not open the page.Please retry in a few minutes"

    status = '200 OK'
    response_headers  =  [('Content-Type', 'text/html;charset=utf-8'),('Content-Length', str(len(html))),('Set-Cookie', cookie)]
    start_response(status, response_headers)

    return html

port = int(os.environ.get("PORT",5000))
httpd = make_server('0.0.0.0',port,application)
httpd.serve_forever()


