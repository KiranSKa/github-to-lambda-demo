import json
import requests
import datetime
import sys
import os

 

def lambda_handler(event, context):
    print('Test')
    print(sys.argv[0])
    #exit()
    #cur_date = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S ")
    sla_days= 4
    desc = os.environ.get('Description')
    start_date = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S ")
#   end_date = str(os.environ.get('end_date'))
    end_date= (datetime.datetime.now() + datetime.timedelta(days=sla_days)).strftime("%m-%d-%Y %H:%M:%S ")
    print(desc)
    print("start_date",start_date)
    print("end_date",end_date)
    client_id = "fZGT2SD2ina02soyAJQzrGHaktwDoJecuV76dyc7NVCpeRIY"
    client_secret = "DOYnrYef0lZ1PCEIbiGNYBaGv5fVFd6V02by8psQrApoNvfb6puqsP6r6ApASEim"
    url ="https://fssfed.stage.ge.com/fss/as/token.oauth2?grant_type=client_credentials&client_id="+client_id+"&client_secret="+client_secret+"&scope=api"
    payload = {}
    headers = {'Cookie': 'PF=qGFkRDj5nW98XKhE1l3mgr'}
    response = requests.request("POST", url, headers=headers, data=payload)
    tk = json.loads(response.text)['access_token']
    print(tk)
    payload1 = { "insert": { "partnerInfo": { "name": "com.aviation.github.cmsspares", "externalRecord": "123456789" }, "type": "Normal", "requested_by": "503371508", "cmdb_ci": "1000379521", "affected_cis": "1000379521", "start_date": "", "end_date": "10/20/2023 11:51:11", "short_description": "This is a test.", "description": "", "justification": "Because this is only a test.", "assigned_to": "503371508", "work_notes": "This is a test. This is only a test." } }
    payload1['insert']['description'] = desc
    payload1['insert']['start_date'] = start_date
    payload1['insert']['end_date'] = end_date
    print(payload1)
    headers = {	'Accept': 'application/json',	'Content-Type': 'application/json',	'Authorization': 'Bearer '+tk  ,	'Cookie': 'PF=qGFkRDj5nW98XKhE1l3mgr; BIGipServerpool_geitqa=914863114.33086.0000; JSESSIONID=27814525AB8DEED59EAEC258C0171226; glide_session_store=B9875435972E6D1032EA30B11153AF4C; glide_user_activity=U0N2M18xOnpDUHcwSXIwRER1UmZqeEZwd1pHK1RiRy9QdDJ5bFZ2bVppTTdyMXpkY0k9Oi9JdzFLeEtnYzNsejYyRHUrWmNxQloxNGJpRjE1QnFOSVU3aEhTQVcxMzA9; glide_user_route=glide.7fbadd483ca755acfea92aede61e0569'	}
    print(headers)
    url1= "https://stage.api.ge.com/digital/servicenowqanormalchange/v1"
    response = requests.request("POST", url1, headers=headers, json=payload1)
    print(response.status_code)
    if(response.ok):
        print(response.text)
        number = json.loads(response.text)['result']['number']
        print(number)
        print(response.text)
        return {
        'statusCode': response.status_code,
        'body': json.dumps('Hello from Lambda!'),
        'tk': json.dumps(tk),
        'ChangeNumber': number
        }
    else:
        return {
        'statusCode': response.status_code,
        'Error': response.reason,
        'body': json.dumps('Hello from Lambda!'),
        'tk': json.dumps(tk)
        }
