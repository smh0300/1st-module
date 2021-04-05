import urllib.request as ur
from bs4 import BeautifulSoup as bs
import pymysql
import re
import datetime
times = datetime.datetime.now()
time = times.strftime('%y.%m.%d %a %H:%M:%S')

def get_jobkorea_hireinfo(url: str) -> list:
    html = ur.urlopen(url)
    soup = bs(html.read(), 'html.parser')
 
    company=soup.find_all('a',{'class':'name dev_view'})
    title=soup.find_all('a',{'class':'title dev_view'})
    date=soup.find_all('span',{'class':'date'})

    for i in range(len(title)):
        cname= company[i].text
        tname= title[i].text.replace("\n","").replace("\r","").lstrip().rstrip()
        lname= 'https://www.jobkorea.co.kr'+company[i].get('href')
        dname= date[i].text.replace("~","").replace("/",".")
        dname2= re.sub("\(.*\)"," ", dname).rstrip()
        sname="Jobkorea"

        hireinfo.append((cname,tname,lname,dname2,sname))
    return hireinfo


def get_saramin_hireinfo(url: str) -> list:
    html = ur.urlopen(url)
    soup = bs(html.read(), 'html.parser')
 
    company=soup.find_all('strong',{'class':'corp_name'})
    title=soup.find_all('h2',{'class':'job_tit'})
    date=soup.find_all('span',{'class':'date'})

    for i in range(len(company)):
        cname= company[i].text
        tname= title[i].text.replace("\n","").rstrip()
        lname= title[i].find('a',{'target':'_blank'}).get('href')
        lname2= 'https://www.saramin.co.kr'+lname
        dname= date[i].text.replace("~","").replace("/",".").replace("채용시","상시채용")
        dname2= re.sub("\(.*\)"," ", dname).rstrip().lstrip()
        sname="Saramin"

        hireinfo.append((cname,tname,lname2,dname2,sname))
    return hireinfo



def insert_table(hireinfo: list):
    try:
        with pymysql.connect(
            host="db",
            port=3306,
            user="3jo",
            password="3jo", 
            charset="utf8", 
            database="3jo"
        ) as connection:
            with connection.cursor() as cursor:
                try:
                    create_hire_table_query = """
                        create table job (
                            id int auto_increment primary key,
                            company varchar(1000),
                            title varchar(1000),
                            link varchar(1000), 
                            end_date varchar(1000),
                            site varchar(1000),
                            time timestamp default now()
                            
                        );
                    """
                    cursor.execute(create_hire_table_query)

                except Exception as e:
                    pass
                
                try:
                    change_charset1 = """
                    ALTER TABLE job CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;
                    """
                    cursor.execute(change_charset1)

                except Exception as e:
                    print(f'[{time}] Error!!! : {e}')

                try:
                    overlap_count = 0
                    for x in range(len(hireinfo)):
                        overlap_check = """select title from job where title like %s"""
                        cursor.execute(overlap_check,hireinfo[x][1])
                        connection.commit()
                        result = cursor.fetchone()
                        if result==None:
                            insert_job = """
                            insert into job (company, title, link, end_date, site)
                            values(%s, %s, %s, %s, %s);
                            """
                            cursor.execute(insert_job,(hireinfo[x][0],hireinfo[x][1],hireinfo[x][2],hireinfo[x][3],hireinfo[x][4]))
                            connection.commit()
                        else:
                            overlap_count += 1

                    if overlap_count != len(hireinfo):
                        print(f'[{time}] [+] \'{hireinfo[0][4]}\' has {len(hireinfo)-overlap_count} new job(s)')
                        # for y,x in enumerate(new_article):
                        #     print(int(y)+1,'  ',x)
                    else:
                        print(f'[{time}] [-] \'{hireinfo[0][4]}\' has no recent job(s)')

                except Exception as e:
                    print(f'[{time}] Error!!! : {e}')

    except Exception as e:
        print(f'[{time}] Error!!! : {e}')

if __name__ == "__main__":
    print('')
    print(f'[{time}] ==================== Job Crawling result ====================')
    hireinfo = []
    hireinfo = get_jobkorea_hireinfo('https://www.jobkorea.co.kr/Search/?stext=IT%EB%B3%B4%EC%95%88&tabType=recruit&Page_No=1')
    hireinfo = get_jobkorea_hireinfo('https://www.jobkorea.co.kr/Search/?stext=IT%EB%B3%B4%EC%95%88&tabType=recruit&Page_No=2')
    hireinfo = get_jobkorea_hireinfo('https://www.jobkorea.co.kr/Search/?stext=IT%EB%B3%B4%EC%95%88&tabType=recruit&Page_No=3')
    insert_table(hireinfo)
    hireinfo = []
    hireinfo = get_saramin_hireinfo('https://www.saramin.co.kr/zf_user/search?search_area=main&search_done=y&search_optional_item=n&searchType=search&searchword=%EC%A0%95%EB%B3%B4%EB%B3%B4%EC%95%88')
    insert_table(hireinfo)