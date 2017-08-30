import sys
sys.path.append('/usr/local/aws/lib/python2.7/site-packages')
import urllib, json
import requests
import boto3
import webbrowser

client = boto3.client('sts')

response = client.assume_role(
    RoleArn='arn:aws-cn:iam::360316469267:role/aws-fed-readonly',
    RoleSessionName='BJS-Readonly',
    DurationSeconds=3600
)

print response['Credentials']

json_string_with_temp_credentials = '{'
json_string_with_temp_credentials += '"sessionId":"' + response['Credentials']['AccessKeyId'] + '",'
json_string_with_temp_credentials += '"sessionKey":"' + response['Credentials']['SecretAccessKey'] + '",'
json_string_with_temp_credentials += '"sessionToken":"' + response['Credentials']['SessionToken'] + '"'
json_string_with_temp_credentials += '}'

request_parameters = "?Action=getSigninToken"
request_parameters += "&Session=" + urllib.quote_plus(json_string_with_temp_credentials)

request_url = "https://signin.amazonaws.cn/federation" + request_parameters

r = requests.get(request_url)

signin_token = json.loads(r.text)

request_parameters = "?Action=login" 
request_parameters += "&Issuer=example.com" 
request_parameters += "&Destination=" + urllib.quote_plus("https://console.amazonaws.cn/")
request_parameters += "&SigninToken=" + signin_token["SigninToken"]

request_url = "https://signin.amazonaws.cn/federation" + request_parameters

#Open default web browser to access AWS BJS console
#webbrowser.open(request_url)
print request_url
