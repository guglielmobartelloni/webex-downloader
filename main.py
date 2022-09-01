import requests
import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from selenium.webdriver.common.keys import Keys
import re

import urllib.request
from tqdm import tqdm



url = "https://lti.educonnector.io/api/webex/recordings"

cookies = {
    'ahoy_visitor': '035461c0-946b-4c6c-ba83-0639be061063',
    'ahoy_visit': 'c4e05e2b-afac-4557-8b20-2e337f5500ef',
    '_ea_involvio_lti_session': 'GiO6vz7haPiVuyCnSdbaUJkffJn710I8AP6ruPJRzbN%2FKLGbozYhcw5bXfw4nG0IyHv6yUND6Kv1Gb3RZUOpy%2BvqR0GElF6gahc0hDtipv%2Bk81UqbA40aJNk5WeQfLiDtOOe85sxTmy1%2B8a%2BCl4gtmXX8TyzxTSKg%2FMtL1SNIPi%2FKUcqPV4ZALPKQDjq6Ur1FsDaubQDocZG2bgNBnMtPRyq%2FhYG4i5LYHrk7V1oCmJT6sSDuqZBBiOV6EHhtv5%2BdvS4oDKyLzdUVgF%2FE2Ymgak4viB29kdVESVaZiVwOS4vTJWBbBwkSkdw4%2BKt4NmcCTKTsUNlf6GE0z5ltO5q%2BpHCR2k%2BgfUw35EV2iONNL0Y%2F8pMHKynfz0%2F9kHc14jC%2BstaP767W9oq3KOKW8o4Ooa%2B1oFk%2B5DprsVRnquZWQKYbjzfcFya41e8iroPDul2uigUfwqKtKZ3qaBEpRG0a5t%2BsDDze0CdtrQYiNkpN8T%2Fhm2%2FXZAz3b6uW8LM48yzHI453ggagnlNY9wCn%2Bf2PTCoRvmmR5bICYcvN39H1tYxY4J3R%2BF8HM3hCvoXW26Yk1lu65SFF6An2IqpsXzFo9YOSo%2Bt6zbpDQ%2B1R00khIGJX%2BHOgCkiobqjPioUylbAQP0T4Z0aD%2F1yVX0sB4p5rTTqDpshi1tRFHghGA%3D%3D--6rEQVR9PXatBUpzu--av3vNCUSm9HsxE1dhsYbgA%3D%3D',
}
payload={}
headers = {
  'authority': 'lti.educonnector.io',
  'accept': 'application/json',
  'accept-language': 'it-IT,it;q=0.5',
  'content-type': 'application/json',
}

response = requests.request("GET", url, headers=headers, data=payload, cookies=cookies)

lesson_list=json.loads(response.text)

params = {
    'siteurl': 'unifirenze',
}

recording_links = open('recording_links.txt', 'a')
for lesson in lesson_list:
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'it-IT,it;q=0.6',
        'Connection': 'keep-alive',
        # Requests sorts cookies= alphabetically
        # 'Cookie': 'trackingSessionID=7686E9C027594B7E9734859844EAB187; _csrf_=2919cf5a-2873-42c4-ab0c-0b9de16820a2; CK_M_ACLK=e8a678ea-ffc8-43f5-84eb-8572c93ec511; NSC_ofcvmbch-ud-80-wjq=756ca3c1218b4e020b8117da070add76fd57055070a6cb9dfce392a8d9279104ea55476d; CK_LanguageID_14673972=10; CK_RegionID_14673972=10; CK_ViewType_14673972=modern; NSC_noh-ch-gsb01-80-wjq=0045a3d25a0592b25b5354292dab4ae41766e4b46ebf6101d5926a72d71ecfab662551f9; wbxsid=95db437c-7cc9-44e0-af8f-c9fa8095fec5; JSESSIONID=911F936C1FFB8F36CBA4DA45B3571FA6; CK_CDNHostStatus=akamaicdn.webex.com|1661948720706|1; ADRUM_BTa=R:85|g:995a1221-2e84-480b-b737-87144298bc3a|n:ciscowebexprod_53fb3051-861d-49c7-baa5-1a751d49b650; SameSite=None; ADRUM_BT1=R:85|i:4023777|e:76',
        # 'Referer': 'https://unifirenze.webex.com/recordingservice/sites/unifirenze/recording/3407a52f7069103a8ffe005056826155/playback',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-GPC': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.102 Safari/537.36',
        # 'appFrom': 'pb',
        'dnt': '1',
        'accessPwd': lesson['password'],
    }
    response = requests.get(lesson['recording_url'])
    url=re.search("(?P<url>https?://[^\s]+)", response.text).group("url")
    lesson_id=url[len("https://unifirenze.webex.com/recordingservice/sites/unifirenze/recording/playback/"):len(url)-2]
    response = requests.get('https://unifirenze.webex.com/webappng/api/v1/recordings/'+lesson_id+'/stream', params=params, cookies=cookies, headers=headers)
    response_json=json.loads(response.text)
    recording_link=response_json['downloadRecordingInfo']['downloadInfo']['mp4URL']
    file_name=response_json['recordName']+".mp4"
    recording_links.write(recording_link + "\n")

# download_file("https://nfg1wss.webex.com/nbr/MultiThreadDownloadServlet?siteid=14673972&recordid=319586842&confid=219360723902310382&from=MBS&trackingID=7686E9C027594B7E9734859844EAB187_1661949306633&language=it_IT&userid=568497462&serviceRecordID=319578207&ticket=SDJTSwAAAAVJrmJe8McLh14jyZrRzeEx2EpmHGPgr4xM3VGgshy9Bw%3D%3D&timestamp=1661958493121&islogin=yes&isprevent=no&ispwd=yes&siteurl=unifirenze.webex.com")

