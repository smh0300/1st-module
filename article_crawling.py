import urllib.request as ur, pymysql, re
from bs4 import BeautifulSoup as bs
import datetime
times = datetime.datetime.now()
time = times.strftime('%y.%m.%d %a %H:%M:%S')

def boannews():
    url = 'https://www.boannews.com/media/t_list.asp'
    with ur.urlopen(url) as r:  
        soup = bs(r.read(),'html.parser')
        article = soup.find_all('div',{'class':'news_list'})
        title, link, image = [], [], []
        for x in article:
            if x.find('img') != None:
                title.append(x.find('span', {'class':'news_txt'}).text)
                link.append('https://www.boannews.com/'+ x.find('a')['href'])
                image.append('https://www.boannews.com/'+ x.find('img')['src'])
            else:
                continue

    return title, link, image, 'boannews'

def dailysecu():
    url = 'https://www.dailysecu.com/news/articleList.html?sc_section_code=S1N2&view_type=sm'
    with ur.urlopen(url) as r:
        soup = bs(r.read(),'html.parser')
        article = soup.find_all('div',{'class':'list-titles'})
        title = [x.text for x in article[:-1]]
        link = ['https://www.dailysecu.com/'+ x.find('a')['href'] for x in article[:-1]]
        article = soup.find_all('div',{'class':'list-image'})[:20]
        image = ['https://www.dailysecu.com/news/photo/' + x['style'][33:-10] + '.jpg' for x in article]

    return title, link, image, 'dailysecu'

def thehackernews():
    url = 'https://thehackernews.com/'
    with ur.urlopen(url) as r:
        soup = bs(r.read(),'html.parser')
        hacker_news = soup.find_all('h2',{'class':'home-title'})
        title = [x.text for x in hacker_news]
        hacker_news = soup.find_all('a',{'class':'story-link'})
        link = [x['href'] for x in hacker_news]
        hacker_news = soup.find_all('div',{'class':'img-ratio'})
        image=[x.find('img')['data-src'] for x in hacker_news]

    return title, link, image, 'TheHackerNews'

def db_connect(title :list, link :list, image: list, homepage :str):
    try:
        with pymysql.connect(
            host="db",
            port=3306,
            user="3jo",
            passwd="3jo", 
            database="3jo",
            charset="utf8"
        ) as connection:
            with connection.cursor() as cursor:
                try:
                    create_table = """
                    create table article (
                        id int auto_increment primary key,
                        title varchar(1000),
                        link varchar(1000),
                        image varchar(1000),
                        homepage varchar(1000),
                        time timestamp default now()
                    );
                    """
                    cursor.execute(create_table)

                except:
                    pass

                try:
                    change_charset1 = """
                    ALTER TABLE article CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
                    """
                    cursor.execute(change_charset1)
                except Exception as e:
                    print(f'[{time}] Error!!! : {e}')

                try:
                    change_charset2 = """
                    ALTER DATABASE 3jo CHARACTER SET utf8 COLLATE utf8_general_ci;
                    """
                    cursor.execute(change_charset2)

                except Exception as e:
                    print(f'[{time}] Error!!! : {e}')

                try:
                    overlap_count = 0
                    new_article = []
                    for x in range(len(title)):
                        overlap_check = """select title from article where title like %s"""
                        cursor.execute(overlap_check,title[x])
                        connection.commit()
                        result = cursor.fetchone()
                        if result == None:
                            new_article.append(title[x])
                            insert_article = """
                            insert into article (title, link, image, homepage)
                            values ( %s, %s, %s, %s );
                            """
                            cursor.execute(insert_article,(title[x],link[x],image[x],homepage))
                            connection.commit()
                        else:
                            overlap_count += 1

                    if overlap_count != len(title):
                        print(f'[{time}] [+] \'{homepage}\' has {len(title)-overlap_count} new article(s)')
                        # for y,x in enumerate(new_article):
                        #     print(int(y)+1,'  ',x)
                    else:
                        print(f'[{time}] [-] \'{homepage}\' has no recent article(s)')

                except Exception as e:
                    print(f'[{time}] Error!!! : {e}')

    except Exception as e:
        print(f'[{time}] Error!!! : {e}')



if __name__ == "__main__":
    print('')
    print(f'[{time}] ==================== Article Crawling result ====================')
    title, link, image, home_page = boannews()
    db_connect(title, link, image, home_page)

    title, link, image, home_page = dailysecu()
    db_connect(title, link, image, home_page)

    title, link, image, home_page = thehackernews()
    db_connect(title, link, image, home_page)
