from bs4 import BeautifulSoup
import requests
import pandas as pd

pd.set_option('display.max_columns', None)


def create_book_df():
    return pd.DataFrame(columns=('year', 'recommendation_category', 'title', 'author'))


def populate_book_df_2020(df):
    url = 'https://www.gatesnotes.com/About-Bill-Gates/Holiday-Books-2020'
    headers = {
        'User-Agent': 'user_access'
    }
    author_list = []
    title_list = []
    html_text = requests.get(url, headers=headers).text
    soup = BeautifulSoup(html_text, 'lxml')
    date = soup.find('div', class_='article_top_dateline')
    books = soup.find_all('div', class_='TGN_Article_ReadTimeSection')
    alldata = soup.select('p > em > a')
    year = date.text.strip()[-4:]
    type = 'Year'
    for data in alldata:
        raw_data = data.text
        if 'by' in raw_data:
            author = raw_data.replace("by ", "")
            author_list.append(author)
        elif ',' == raw_data.strip():
            pass
        else:
            title = raw_data
            title_list.append(title)
    for title, author in zip(title_list, author_list):
        df = df.append({'year': year, 'recommendation_category': type, 'title': title, 'author': author},
                       ignore_index=True)
    return df


def populate_book_df_2021(df):
    url_year_2021 = 'https://www.gatesnotes.com/About-Bill-Gates/Holiday-Books-2021'
    url_summer_2021 = 'https://www.gatesnotes.com/About-Bill-Gates/Summer-Books-2021'
    url_list_2021 = [url_year_2021, url_summer_2021]
    headers = {
        'User-Agent': 'user_access'
    }
    for url in url_list_2021:
        html_text = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html_text, 'lxml')
        date = soup.find('div', class_='article_top_dateline')
        books = soup.find_all('div', class_='TGN_Article_ReadTimeSection')
        titles = soup.select('p > strong > em > a')
        authors = soup.select('p > em > a')
        for title, author in zip(titles, authors):
            title_name = title.text.replace(",", "")
            author_name = author.text
            author_name = author_name.replace("by ", "")
            year = date.text.strip()[-4:]
            if 'Summer' in url:
                type = 'Summer'
            else:
                type = 'Year'
            df = df.append({'year': year, 'recommendation_category': type, 'title': title_name, 'author': author_name},
                           ignore_index=True)
    return df


empty_df = create_book_df()
df = populate_book_df_2021(empty_df)
print(populate_book_df_2020(df))

