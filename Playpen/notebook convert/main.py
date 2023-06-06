# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import pandas as pd
from bs4 import BeautifulSoup
import json
import urllib.request

def convert_html():

    url = 'file:///D:/Robert/OneDrive/Documents/0%20Coursework/CQF/Jupyter%20Notebooks/Python%20Lab%202%20-%20Binomial%20Trees/Jan%2022%20cohort/02-Binomial-Model.html'
    response = urllib.request.urlopen(url)
    #  for local html file
    # response = open("/Users/note/jupyter/notebook.html")
    text = response.read()

    print(text)

    soup = BeautifulSoup(text, 'lxml')
    # see some of the html
    print(soup.div)
    dictionary = {'nbformat': 4, 'nbformat_minor': 1, 'cells': [], 'metadata': {}}
    for d in soup.findAll("div"):
        if 'class' in d.attrs.keys():
            for clas in d.attrs["class"]:
                print(f"clas is {clas}")
                print(d.get_text())
                if clas in ["text_cell_render", "input_area", "jp-RenderedHTMLCommon jp-RenderedMarkdown jp-MarkdownOutput ", "jp-Cell-inputWrapper", "jp-InputPrompt", "jp-InputArea-prompt"]:

                    # code cell
                    if clas == "jp-Cell-inputWrapper":
                        cell = {}
                        cell['metadata'] = {}
                        cell['outputs'] = []
                        cell['source'] = [d.get_text()]
                        cell['execution_count'] = None
                        cell['cell_type'] = 'code'
                        dictionary['cells'].append(cell)

                    else:
                        cell = {}
                        cell['metadata'] = {}

                        cell['source'] = [d.decode_contents()]
                        cell['cell_type'] = 'markdown'
                        dictionary['cells'].append(cell)

    print('now opening the notebook i think')
    open('notebook.ipynb', 'w').write(json.dumps(dictionary))



def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    convert_html()

def search_bbc():
    import requests
    import re
    from bs4 import BeautifulSoup
    from datetime import datetime

    # Define start and end dates for the news search
    start_date = datetime.strptime("2022-03-18", "%Y-%m-%d")
    end_date = datetime.now()

    # Search for "Credit Suisse" news stories
    base_url = "https://www.bbc.co.uk/search?q=credit+suissse&filter=news&page={}"
    page_number = 1
    links = []
    dates = []
    while True:
        url = base_url.format(page_number)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract links to news stories and their publication dates
        for link in soup.find_all("a", href=True):
            href = link.get("href")
            if href.startswith("http") and "www.bbc.co.uk/" in href and "/news/" in href:
                date_str = link.find_parent("div", class_="gl__date").text.strip()
                try:
                    date = datetime.strptime(date_str, "%d %b %Y")
                except ValueError:
                    continue  # skip articles with invalid date strings
                if start_date <= date <= end_date:
                    links.append(href)
                    dates.append(date)

        # Check if there is a next page of search results
        next_link = soup.find("a", class_="pagination-next")
        if not next_link:
            break  # we've reached the end of the search results
        else:
            page_number += 1

    # Extract text from each news story
    for link, date in zip(links, dates):
        response = requests.get(link)
        soup = BeautifulSoup(response.content, "html.parser")
        article = soup.find("article")
        if article and "Credit Suisse" in article.text:
            print(f"{date.date()}: {article.text.strip()}\n")

def search_bbc_2():
    import requests
    from bs4 import BeautifulSoup

    # define the search query
    query = "Credit Suisse"

    # loop through the first 10 pages of the search results
    for page_num in range(1, 11):
        # create the url for the current page of search results
        url = f"https://www.bbc.co.uk/search?q={query}&page={page_num}"
        # send a GET request to the url and get the response
        response = requests.get(url)
        # parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # find all the links on the page
        links = soup.find_all('a')
        # loop through the links
        for link in links:
            # get the URL of the link
            url = link.get('href')
            # check if the link is a news article
            if '/news/' in url:
                # send a GET request to the news article url and get the response
                article_response = requests.get(url)
                # parse the HTML content of the response using BeautifulSoup
                article_soup = BeautifulSoup(article_response.content, 'html.parser')
                # find the main article content and print it
                # article_content = article_soup.find('div', class_='story-body__inner').get_text()
                article_content = article_soup.text
                # print(article_content)
                # print(article_soup.prettify())

                # span_date = article_soup.find('span', {'class': 'item_date'})
                # if span_date:
                #     date = span_date.get_text()
                #     print(date)
                # else:
                #     print(f'Unable to identify date for this article {url}')
                #
                # article_pub_date = article_soup.find('div', class_='date')
                # if article_pub_date:
                #     print(f'got a date! {article_pub_date}')
                # else:
                #     print(f'can\'t get a date')

                # print('attempting to get date via requests')
                # import requests
                # r = requests.get(url)
                # if 'Last-Modified' in response.headers:
                #     last_modified = response.headers['Last-Modified']
                #     print(f'The web page was last modified on {last_modified}.')
                # else:
                #     print('The web page does not include a Last-Modified header.')

                # response = requests.get(url)
                #
                # if response.status_code == 200:
                #     s = BeautifulSoup(response.content, 'html.parser')
                #     last_modified_tag = s.find('meta', attrs={'name': 'last-modified'})
                #     if last_modified_tag is not None and 'content' in last_modified_tag.attrs:
                #         last_modified = last_modified_tag['content']
                #         print(f'The web page was last modified on {last_modified}.')
                #     else:
                #         print('The web page does not include a last-modified tag.')
                # else:
                #     print('Unable to access the web page.')
                #
                # import requests
                #
                # # Make an initial GET request to get the ETag header
                # response = requests.get(url)
                #
                # if response.status_code == 200:
                #     etag = response.headers.get('ETag')
                #
                #     # Make a conditional GET request with the ETag header
                #     headers = {'If-None-Match': etag}
                #     response = requests.get(url, headers=headers)
                #
                #     if response.status_code == 200:
                #         # The web page has been updated
                #         # Process the updated content
                #         pass
                #     elif response.status_code == 304:
                #         # The web page has not been updated
                #         # No need to process the content
                #         pass
                #     else:
                #         # Unable to access the web page
                #         pass
                # else:
                #     # Unable to access the web page
                #     pass
                #
                # import requests
                # from bs4 import BeautifulSoup
                #
                # # url = 'https://www.bbc.co.uk/news/world-europe-61185028'
                #
                # response = requests.get(url)
                #
                # if response.status_code == 200:
                #     soup = BeautifulSoup(response.content, 'html.parser')
                #     time_tag = soup.find('time', {'class': 'qa-story-timestamp'})
                #     if time_tag:
                #         last_update = time_tag['datetime']
                #         print(f'The article was last updated on {last_update}.')
                #     else:
                #         print('Unable to find the last update datetime.')
                # else:
                #     print('Unable to access the article page.')

                soup = BeautifulSoup(response.content, 'html.parser')
                time_tag = soup.find('time', {'class': 'dateTime'})

                # i just want something to add a breakpoint to :)
                jim = 42

def search_bbc_3():
    import requests
    from bs4 import BeautifulSoup

    # define the search query
    query = "Credit Suisse"

    results = pd.DataFrame(columns=['date','contents'])

    # loop through the first 10 pages of the search results
    for page_num in range(1, 11):
        print(f'now doing page {page_num}')
        # create the url for the current page of search results
        url = f"https://www.bbc.co.uk/search?q={query}&page={page_num}"
        # send a GET request to the url and get the response
        response = requests.get(url)
        # parse the HTML content of the response using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        # find all the links on the page
        links = soup.find_all('a')
        # loop through the links
        for link in links:
            # get the URL of the link
            url = link.get('href')
            # check if the link is a news article
            if '/news/' in url:
                # send a GET request to the news article url and get the response
                article_response = requests.get(url)
                # parse the HTML content of the response using BeautifulSoup
                article_soup = BeautifulSoup(article_response.content, 'html.parser')
                # find the main article content and print it
                # article_content = article_soup.find('div', class_='story-body__inner').get_text()
                article_content = article_soup.text

                soup = BeautifulSoup(article_response.content, 'html.parser')
                time_element = soup.find('time', {'data-testid': 'timestamp'})
                if (time_element):
                    datetime_value = time_element['datetime']
                    print(f'URL {url} has datetime of {datetime_value}')
                    results = results.append({'date': datetime_value, 'contents': '"' + article_content + '"'}, ignore_index=True)
                else:
                    print(f'Unable to identify a datetime for url {url}')

    results.to_csv('./bbcresults.csv', sep='|')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print_hi('PyCharm')
    # search_bbc()
    # search_bbc_2()

    # jim = pd.DataFrame(columns=['date','contents'])
    # jim = jim.append({'date': '2023-04-10', 'contents': 'hello'}, ignore_index=True)
    # print(jim.head())
    search_bbc_3()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
