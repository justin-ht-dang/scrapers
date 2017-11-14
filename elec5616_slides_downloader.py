import requests, ssl, time, os
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urljoin

def download_pdf(url, path):

    response = requests.get(url)
    with open(path, 'wb') as f:
        f.write(response.content)


def select_url(lst):

    lst = filter(None, lst)
    selected = [i for i in lst if 'static/lectures' in i and i.endswith('.pdf')]

    return selected


def get_links(url):

    #bypassing ssl verification (apparently it's a discouraged temp workaround)
    context = ssl._create_unverified_context()

    page = urlopen(url, context=context)
    soup = BeautifulSoup(page, 'html.parser')

    url_list = []

    for link in soup.find_all('a'):
        url_list.append(urljoin(url, link.get('href')))

    return url_list


def main():

    url_list = select_url(get_links('https://elec5616.com/lectures.html'))

    if not os.path.exists('lectures'):
        os.makedirs('lectures')

    lecture_count = 1

    for pdf in url_list:

        #download_pdf(pdf, './lectures/lecture' + str(lecture_count))

        print('Lecture ' + str(lecture_count) + ' downloaded')
        lecture_count += 1

        time.sleep(1)

    print('Download completed!')


if __name__ == "__main__":
    main()
