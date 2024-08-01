from celery import shared_task
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from tecnews.models import TagModel, NewModel
@shared_task()
def get_news_url(archive_page_number):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')

    driver = webdriver.Chrome(options=options)
    news_url = []
    try:
        archive_page_url = f"https://www.zoomit.ir/archive/?sort=Newest&publishPeriod=All&readingTimeRange=All&pageNumber={archive_page_number}"
        driver.get(archive_page_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        driver.quit()
        news = soup.find_all('a', class_="link__CustomNextLink-sc-1r7l32j-0 eoKbWT BrowseArticleListItemDesktop__WrapperLink-zb6c6m-6 bzMtyO")
        for item in news:
            news_url.append(item['href'])
        return news_url
    except Exception as e:
        print(e)
        return []

@shared_task()
def scraper1():
    archive_page_number = 1
    find_new_news = True
    while find_new_news :
        ses = requests.Session()
        news_url = get_news_url(archive_page_number)
        if not news_url:
            print("Page does not have URL")
            continue
        for url in news_url:
            title = ""
            try:
                new_page = ses.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
                soup = BeautifulSoup(new_page.content, 'html.parser')
                title = soup.find('h1', class_="typography__StyledDynamicTypographyComponent-t787b7-0 fzMmhL").text

                if NewModel.objects.filter(Title=title).exists():
                    return ("End of task. no new news find")
                    find_new_news = False
                    break

                tag_box = soup.find('div', {'class': "flex__Flex-le1v16-0 kDyGrB"})
                new_tags_html = tag_box.find_all('a', {'class': "link__CustomNextLink-sc-1r7l32j-0 cczRGt"})
                new_tags = [tag.text for tag in new_tags_html]

                new_text_html = soup.find_all('p', {
                    'class': "typography__StyledDynamicTypographyComponent-t787b7-0 fZZfUi ParagraphElement__ParagraphBase-sc-1soo3i3-0 gOVZGU"})
                new_text = ""
                for element in new_text_html:
                    new_text += element.text + "\n"

                new_source_html = soup.find('a', {'rel': 'nofollow'})
                new_source = new_source_html.get('href') if new_source_html else ""

                # Save to database
                news = NewModel(Title=title, Text=new_text, Source=new_source)
                news.save()
                for tag in new_tags:
                    tag_obj, created = TagModel.objects.get_or_create(Name=tag)
                    news.Tags.add(tag_obj)
                news.save()
                print("news foound")
            except Exception as e:
                print(f"Error processing {url}: {e}")
        archive_page_number +=1







