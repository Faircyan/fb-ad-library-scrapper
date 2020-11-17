import requests
from django.urls import path
from django.http import HttpResponse

PageLink = 'https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&view_all_page_id=100403665194082'

PublisherName = "Default"
MaxAdCount = 1
list = []
PageId = '527358433996753'


class GameClass:
    AppStoreLink = ""
    Videos = []
    Counter = 0


def ClearLink(link):
    return link.split("&sort_data")[0]


def ControlList(link):
    for i in list:
        if i.AppStoreLink == link:
            return True

    return False


def GetList(link):
    for i in list:
        if i.AppStoreLink == link:
            return i


def AddList(link):
    game = GameClass()
    game.Videos = []
    game.AppStoreLink = link
    list.append(game)


def CreateData(page_id):
    forwardcursor = ''
    file = ""
    # for i in range(0, MaxAdCount):

    url = 'https://www.facebook.com/ads/library/async/search_ads/'
    myobj = {'__user': '0', '__a': '1'}

    params = {'session_id': '3a5fc85c-ffcc-4dc5-993c-175a3e2f690f', 'count': '30', 'active_status': 'all',
                'ad_type': 'all', 'countries[0]': 'ALL', 'view_all_page_id': page_id}
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'}

    cookies = {}
    x = requests.post(url, params=params, headers=headers, data=myobj, cookies=cookies)

    file = x.text

        # if len(x.text.split("forwardCursor")) > 1:
        #     forwardcursor = x.text.split("forwardCursor")[1].split(',')[0].strip('"').strip(':').strip('"')
        # else:
        #     forwardcursor = "null"

        # if forwardcursor == "null":
        #     return file
    return file

def GameContainsVideo(game, url):
    for i in game.Videos:
        if url == i:
            return True
    return False


def GetAppName(link):
    AppStore = requests.post(link, params={}, data={}, cookies={})
    GooglePlay = requests.get(link, params={}, data={}, cookies={})
    dataAppStore = AppStore.text
    dataGooglePlay = GooglePlay.text

    tempName = dataAppStore.split('<meta property="og:title" content="‎')
    tempName2 = dataAppStore.split('location.replace("')
    tempName3 = dataAppStore.split('<span class="_5slv">')
    tempName4 = dataGooglePlay.split('<h1 class="AHFaub" itemprop="name"><span')

    if len(tempName) > 1:
        return tempName[1].split('"')[0]
    elif len(tempName2) > 1:
        return GetAppName(tempName2[1].split('"')[0].replace('\\', ''))
    elif len(tempName3) > 1:
        return GetAppName(tempName3[1].split('<')[0].replace('\\', ''))
    elif len(tempName4) > 1:
        return tempName4[1].split('>')[1].split('<')[0]
    else:
        return link


def CreateNames(data):
    names = []
    for i in data['Games']:
        #names.append("Game")
        names.append(GetAppName(i['GameLink']))
    return names


def CreateJson():
    data = {}
    data['Games'] = []
    for i in list:
        data['Games'].append({
            'GameLink': i.AppStoreLink,
            'Counter': i.Counter,
            'Videos': i.Videos
        })
    return data


def FilterData(lines):
    counter = 0
    for i in lines:
        link = i.split('"')[0].replace('\\', '')
        counter += 1
        if not ControlList(link):
            AddList(link)

        game = GetList(link)
        for j in range(len(i.split('"video_sd_url":"'))):
            if j == 1:
                videoUrl = i.split('"video_sd_url":"')[1].split('"')[0].replace('\\', '')
                if not GameContainsVideo(game, videoUrl):
                    game.Videos.append(videoUrl)
                    game.Counter += 1


def SetPublisherName(lines):
    pageNameTemp = lines[0].split('"pageName":"')
    if len(pageNameTemp) > 1:
        return pageNameTemp[1].split('"')[0]


def DownloadData(link):

    data = CreateData(link)

    lines = data.split('"link_url":"')

    publisherName = SetPublisherName(lines)

    lines.pop(0)

    FilterData(lines)

    data = CreateJson()

    names = CreateNames(data)
    return names, data, publisherName