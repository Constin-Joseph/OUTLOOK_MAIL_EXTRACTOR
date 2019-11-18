from requests.models import PreparedRequest
import urllib.request
import json
def apipara(a):
    req = PreparedRequest()
    url = "http://integra-net4/BMJ_ICE_Test/assignjob"
    params = {'ID':a}
    req.prepare_url(url, params)
    content = urllib.request.urlopen(req.url).read()
    data = json.loads(content)
    return data['success'],data['msg']
   


