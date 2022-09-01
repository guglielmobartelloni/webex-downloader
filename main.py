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


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_file(url, file_name):
    print(url)
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=file_name) as t:
        urllib.request.urlretrieve(url, filename=file_name, reporthook=t.update_to)


url = "https://lti.educonnector.io/api/webex/recordings"

payload={}
headers = {
  'authority': 'lti.educonnector.io',
  'accept': 'application/json',
  'accept-language': 'it-IT,it;q=0.5',
  'content-type': 'application/json',
  'cookie': 'ahoy_visitor=035461c0-946b-4c6c-ba83-0639be061063; ahoy_visit=ab0e6a7d-e859-40df-bbcf-d28c03ade36c; _ea_involvio_lti_session=p4xmeywJMmyGcLQd3GWsuYULvFIOywudZh4CQpA3nS%2F2Xf7AXm5uIuoccqWNPxxPMRaLuUL6be24ARUskmd1xtY8CEB7wdoKI6eFpSEh5JT6UBVkg394d6xuezXsXY0JVfAEe7pHWjNzoqav0bIZ6iBn7o%2BgH74rf5c0nons%2FkkYflsZ1XbvEbxQqtCpTpP00EyRVr1%2F81MCORKf%2FnZgRXFq9awSkN5iG6Q92YHbFusMZ01qpzHpbHMsNHbOZ2gEB%2F2lNJRA6%2BUAyGeytfWldy4%2FZYO333Hfzf%2BpVKD4NVvbtBDbo1RFUHRUu7MzHaOMJH%2FGl1%2FMG%2BxJRErMNaHdcQE9gfhVRXLZFMVRqdnXtlpHpoLxTh%2FKA1RFefnNwfp0GIqDiC%2FTHGu7sjoHNwzL2Ytel6MUClV4rPh31S5aBkTa4pmgBy0rm297htA5c%2FxSzP8r613J3yIYSCABVFXFgRGJTX9JFVY1dBQBO5VBQuSgzzjOsdxugbEA%2B9CQgrs4GhjllY5foPxyOgYJoAH%2FFl7ivYEG1XalSFlgqZKELpIIAHgZGDHzja6YCFHVQYjV9uxjIV0IoRCM%2FynIVkEo8imE%2Fx2uoAJJNC140SoxUEH6n2Ndkb1NejOQcQWeS3Mau9bwFEKCHzkJNfohQi%2BIIlQPipmcJdns3eApzA%3D%3D--uvrQiNap0ZKGdblr--RfF%2B3fVyeRG1LDT4RbRIBw%3D%3D; _ea_involvio_lti_session=OKSmsXK5WDg%2BG4Zuhfn6W4j%2B1W4b%2B7RqypGN0YqwuSLfm24MCLzQtehCOskdYwFmowCLtnefG71grhf9nUrpRgNy%2FNqL2QPzzbEbh9VNJEF6tSqv%2FCj7j3VxpemgJEu9ecpouUU44ZGPwYQTQrZcr7hSDnB6aQ6n2cs4WlcJ%2BdEyccDGjV4u5k6awkeGYX%2BLlsxAW5CIQ%2FBh%2Bwdqg0%2FQEm5T9SoUHVm7r3FfCGQQIywmCalEM2BAtwquZio%2FhdmjLEaSO8MXO4yR9Ofo8WCyD6p7JGJaRBUFqgmm%2BK1yVCX5hKKAKbE1zry15kLgkCeWu%2FslOTWge7ZewWWTD2adVgX8GKWs4n0LRSsgjD0OXgkR%2FfHOStE%2F0bsSjFChiHK2uHpIv9HD%2BdFE%2FQeq9yd9VxVqmVKIhyf%2Fl75DnL1Ntb%2BqHbWFzCOFRp%2B7IBifWxGYt4kmcZyR9yPC6%2FKiUuJy4GbQX63lnfOclOMOdkzHiK4QPb8QEjFU6Hqs4WGi%2BPELCs5VKBLFi%2BdmjU8H9UeoNSr163H1S20FqkyJVIIdxi9LhY1XZBrtKsmeyMtueauEMJ%2FbhJhyxeK62vUZFuifiR3URxXQzBg80j0swL1zayf60FHDBlKfyeP%2FjPdu3EUJKqrvUR6XgvW6F47aNbaQErPSvHcjREg2%2FDVIQw%3D%3D--TlGqOjxF%2FHx1NgBd--ZCLflkGFTndDJUp4za65UA%3D%3D; ahoy_visit=ab0e6a7d-e859-40df-bbcf-d28c03ade36c'
}

response = requests.request("GET", url, headers=headers, data=payload)

lesson_list=json.loads(response.text)

cookies = {
    'ahoy_visitor': '035461c0-946b-4c6c-ba83-0639be061063',
    'ahoy_visit': '62dc415a-e422-4a6f-891b-f620e96ffac9',
    '_ea_involvio_lti_session': 'QTHw12%2FvM82rJ2uCPk%2BxT%2BtY%2FOpsyRFKK3sgrG9aHL96eyDrzaUeBJ4A0qT9JpMlorP7uC%2ByQJiPdVI5Oex4NMpPs3d0KlwkDUje6wZBhSRD1L63uLpuYn2gZEu5LtZNr8nLFJ1Mes02BnsQSWLXUT3G0%2BSZJJ8Bbcpp5iUPv2SVFo%2Foog9wUfvdgMxq1g%2F0bsnR6SKnUsxZRczhor39vm0KzZdCTpCSs8LpHQijHT7ZiUdXg7LCZJK4eS1jt%2BlHhFDqBNAYZGhs0O5xmLIJGw6TmQsZK6%2F7AozWhaAXhnXdvgyFyrNUeHiv%2Fz11naiKxtn8HVH8l%2FC%2BImmIFsRSWTbsPlALQeFahlsPekxlVJ4VGg2tAoNbe2MY7Dx7XkcV6vzn%2FeAhn3wE8A7fHwKVq45LV7Xjs4IqNsvWzY8bZIl86ZU%2BR6t06I8UKRaAThux01v%2FgFaxkOJqL1LBpvJsaehHRMoaPlwRZdlGlZ%2FLQLEyfxOOsVxk05VuP31orWzLVL01jY55rmkutb64%2BNK8UeMlfg%2BFPcR9Im1t%2BhPMEAn1GD70dQOPl3qETAsX5mgyJIFrGCcvBl3F7%2Bg4%2BU6Tm1V5SZrW6o%2B0Of87H2lARzIms%2F79v57fjSYw8tQ3IAP1eUjg11UubU1Ik867D7kntwC7LfhEhftEFDD9cQ%3D%3D--PFF0drxBd3%2F9zprA--6pEphbHE%2BtY62r3OqDkGug%3D%3D',
}


params = {
    'siteurl': 'unifirenze',
}


for i,lesson in enumerate(lesson_list):
    if i == 2:
        break
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
    print(url)
    lesson_id=url[len("https://unifirenze.webex.com/recordingservice/sites/unifirenze/recording/playback/"):len(url)-2]
    response = requests.get('https://unifirenze.webex.com/webappng/api/v1/recordings/'+lesson_id+'/stream', params=params, cookies=cookies, headers=headers)
    response_json=json.loads(response.text)
    recording_link=response_json['downloadRecordingInfo']['downloadInfo']['mp4URL']
    file_name=response_json['recordName']+".mp4"
    download_file(recording_link,file_name)

# download_file("https://nfg1wss.webex.com/nbr/MultiThreadDownloadServlet?siteid=14673972&recordid=319586842&confid=219360723902310382&from=MBS&trackingID=7686E9C027594B7E9734859844EAB187_1661949306633&language=it_IT&userid=568497462&serviceRecordID=319578207&ticket=SDJTSwAAAAVJrmJe8McLh14jyZrRzeEx2EpmHGPgr4xM3VGgshy9Bw%3D%3D&timestamp=1661958493121&islogin=yes&isprevent=no&ispwd=yes&siteurl=unifirenze.webex.com")

