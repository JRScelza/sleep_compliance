import json
import tornado.httpclient
import tornado.options
from tornado.options import define, options

define("endpoint",
       type    = str,
       default = 'production',
       help    = "which endpoint to connect: local, dev, production"
)
define("token",
       type    = str,
       help    = "study access token"
)

endpoints = dict(
    local='http://api.ouraring.loc:23450/api/v1',
    dev='https://api.ouracloud.com/api/v1',
    production='https://api.ouraring.com/api/v1'
)

def main(study_uid):
    baseurl = endpoints[options.endpoint]
    client = tornado.httpclient.HTTPClient()

    # 1. Fetch study data as json
    url = '{}/study/{}?access_token={}'.format(
        baseurl, study_uid, options.token
    )
    try:
        response = client.fetch(url)
        data = json.loads(response.body.decode('utf8'))
    except tornado.httpclient.HTTPError as e:
        print("HTTP Error when fetching study data", e)
        client.close()
        return
    except Exception as e:
        print("Error: ", e)
        client.close()
        return

    # pretty print data to the console
    print(json.dumps(data, indent=4, sort_keys=True))

#     2. Fetch latest json url for each participant
    urls = dict()
    for p in data['participants']:
         participant_uid = p['uid']
         email = p['email']
         try:
             url = '{}/study/{}/participant/{}/latest_json_url?access_token={}'.format(
                 baseurl, study_uid, participant_uid, options.token
             )
             response = client.fetch(url)
             data = json.loads(response.body.decode('utf8'))
             print(data)
             urls[email] = data['url']

         except tornado.httpclient.HTTPError as e:
             print("HTTP Error when fetching the latest url: ", e)
         except Exception as e:
             print("Error: ", e)

#     3. Fetch the actual JSON for each participant
    for email, url in urls.items():
         print('fetching JSON for', email)
         response = client.fetch(url)
         outfilename = email.replace('@', '_') + '.json'
         print("writing", outfilename)
         with open('./' + outfilename, 'wb') as outfile:
             outfile.write(response.body)

    client.close()

if __name__=='__main__':
    args = tornado.options.parse_command_line()
    main(args[0])
