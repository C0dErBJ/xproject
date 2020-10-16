from bs4 import BeautifulSoup
import pymysql

db = pymysql.connect("localhost", "root", "12345678aA!", "test")


def getContent():
    cursor = db.cursor()
    cursor.execute(
        'select a.id,a.content,a.name from switch a left join source s on a.id = s.switchid where s.switchid is null')
    shareds = cursor.fetchall()
    contents = []
    for item in shareds:
        ct = {}
        ct['switchid'] = item[0]
        ct['content'] = item[1]
        ct['name'] = item[2]
        contents.append(ct)
    return contents


def parse(contents):
    swtichSource = []
    for ct in contents:
        soup = BeautifulSoup(ct['content'])
        links = soup.find_all("a")
        for ln in links:
            linkSoup = ln
            linkText = linkSoup.get_text().lower()
            if(linkText.find(ct['name'].lower()) != -1):
                torrentSource = {}
                torrentSource['torrent'] = linkSoup.get('href')
                torrentSource['switchid'] = ct['switchid']
                swtichSource.append(torrentSource)
        for tr in soup.find_all('tr'):
            source = {}
            trSoup = tr
            tds = trSoup.find_all(name='td', recursive=False)
            if(len(tds) < 3):
                continue
            source['name'] = tds[0].get_text()
            # source['type'] = tds[1].get_text()
            source['size'] = tds[1].get_text()
            source['switchid'] = ct['switchid']
            tdlinks = tds[2].find_all("a")
            for link in tdlinks:
                text = link.get_text().lower()
                if(text == 'uptobox'):
                    source['uptobox'] = link.get('href')
                if(text == 'gdrive'):
                    source['gdrive'] = link.get('href')
                if(text == 'mega'):
                    source['mega'] = link.get('href')
                if(text == '1fichier'):
                    source['1fichier'] = link.get('href')
                if(text == 'mediafire'):
                    source['mediafire'] = link.get('href')
            swtichSource.append(source)
    return swtichSource


def insert(sources):

    cursor = db.cursor()
    for s in sources:
        torrent = ''
        gdrive = ''
        uptobox = ''
        mega = ''
        fichier = ''
        mediafire = ''
        switchid = ''
        name = ''
        size = ''
        switchtype = ''
        if(s.__contains__('torrent')):
            torrent = s['torrent']
        if(s.__contains__('gdrive')):
            gdrive = s['gdrive']
        if(s.__contains__('uptobox')):
            uptobox = s['uptobox']
        if(s.__contains__('mega')):
            mega = s['mega']
        if(s.__contains__('1fichier')):
            fichier = s['1fichier']
        if(s.__contains__('mediafire')):
            mediafire = s['mediafire']
        if(s.__contains__('switchid')):
            switchid = s['switchid']
        if(s.__contains__('name')):
            name = s['name']
        if(s.__contains__('size')):
            size = s['size']
        if(s.__contains__('switchtype')):
            switchtype = s['switchtype']
        cursor.execute('insert into source(torrent, gdrive, uptobox, mega, `1fichier`, mediafire, switchid, name, size, type) \
 value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (torrent, gdrive, uptobox, mega, fichier, mediafire, switchid, name, size, switchtype))
        db.commit()

if __name__ == "__main__":
    contents = getContent()
    source = parse(contents)
    insert(source)
