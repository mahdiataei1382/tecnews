import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from multiprocessing import Pool
from tecnews.models import TagModel, NewModel

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

def process_page(archive_page_number):
    ses = requests.Session()
    news_url = get_news_url(archive_page_number)
    if not news_url:
        print("Page does not have URL")
        return
    for url in news_url:
        title = ""
        try:
            new_page = ses.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'})
            soup = BeautifulSoup(new_page.content, 'html.parser')
            title = soup.find('h1', class_="typography__StyledDynamicTypographyComponent-t787b7-0 fzMmhL").text

            if NewModel.objects.filter(Title=title).exists():
                print(title)
                return

            tag_box = soup.find('div', {'class': "flex__Flex-le1v16-0 kDyGrB"})
            new_tags_html = tag_box.find_all('a', {'class': "link__CustomNextLink-sc-1r7l32j-0 cczRGt"})
            new_tags = [tag.text for tag in new_tags_html]

            new_text_html = soup.find_all('p', {'class': "typography__StyledDynamicTypographyComponent-t787b7-0 fZZfUi ParagraphElement__ParagraphBase-sc-1soo3i3-0 gOVZGU"})
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

        except Exception as e:
            print(f"Error processing {url}: {e}")
    print(archive_page_number)
def main_scraper():
    max_page_number = 500
    num_workers = 5
    pages_per_worker = max_page_number // num_workers
    page_ranges = [(i * pages_per_worker + 1, (i + 1) * pages_per_worker) for i in range(num_workers)]

    with Pool(num_workers) as pool:
        pool.starmap(scrape_range, page_ranges)

def scrape_range(start_page, end_page):
    for page_number in range(start_page, end_page + 1):
        process_page(page_number)

if __name__ == "__main__":
    main_scraper()
