import webapp2
import jinja2
import sys
import os
import oauth
import urllib
import json
import logging
from google.appengine.api import urlfetch

jinja_environment = jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader( os.path.join(os.path.dirname(__file__), 'templates') ))
    
consumer_key = u'o7hQyqC0Ba8csgohX4sPsQ'
consumer_secret = u'HSyl9wxdaZwHpvolAWEDxdFDMrmKxla2hStLGNbSllM'
access_token  = u'26635865-ug3bmGiHmLGxEhSBIQkRPOEzJ7ZiEX5oP298qPF6U'
token_secret = u'1bPjIMR9EulJB7Uvb8XkNH6tTnEVKGvGYDv4pnt1Ds'
consumer = oauth.OAuthConsumer(consumer_key, consumer_secret)
token = oauth.OAuthToken(access_token, token_secret)
signature_method_hmac_sha1 = oauth.OAuthSignatureMethod_HMAC_SHA1()

class BasicHandler(webapp2.RequestHandler): 
    def get(self):
        template_values = {}
        template = jinja_environment.get_template('basic.html')
        self.response.out.write(template.render(template_values))

class WebHandler(webapp2.RequestHandler): 
    def get(self):
        
        template_values = {}
        template = jinja_environment.get_template('web.html')
        self.response.out.write(template.render(template_values))
        
class twitterHandler(webapp2.RequestHandler):
    def get(self):
        count = int(self.request.get("count", default_value=50))
        since = self.request.get("since", default_value=12345)
        name = self.request.get("name", default_value="cnn")
        names = name.split(',')
        url = u"https://api.twitter.com/1.1/statuses/user_timeline.json"
        ret = []
        for n in names:
            logging.info(n)
            parameters = {
                "screen_name" : n,
                "count" : count}
            oauth_request = oauth.OAuthRequest.from_consumer_and_token(
                consumer, 
                token=token, 
                http_method='GET', 
                http_url=url,
                parameters = parameters)
            oauth_request.sign_request(signature_method_hmac_sha1, consumer, token)
            if parameters:
                url2 = url + "?" + urllib.urlencode(parameters)
            result = urlfetch.fetch(
                url=url2,
                headers=oauth_request.to_header(),
                method=urlfetch.GET)
            if result.status_code == 200:
                ret.extend(json.loads(result.content))
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(ret)) 
        
app = webapp2.WSGIApplication([
    ('/', BasicHandler),
    ('/web', WebHandler),
    ('/tapi', twitterHandler),
    ],debug=True)