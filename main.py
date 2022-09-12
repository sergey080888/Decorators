import os
import datetime
import requests
import re
import bs4
KEYWORDS = ['дизайн', 'фото', 'web', 'python']
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/53.0.2785.143 Safari/537.36'
}


def full_pass():
    base_path = os.getcwd()
    foldrer_name = "logs"
    file_name = 'result.txt'
    return os.path.join(base_path, foldrer_name, file_name)


def decorator(input_arg):
    def logger2(some_function):
        def logger(*args):
            date_ = datetime.datetime.now()
            message = (f'Имя функции: {some_function.__name__} Дата и время вызова функции: {date_},\n'
                  f'аргументы функции:{args},\n')
            with open(input_arg, 'a', encoding="utf-8") as file_obj:
                file_obj.write(message)
            print(message)
            result = some_function(*args)
            return result
        return logger
    return logger2


# декоратор с параметром
@decorator(full_pass())
def scrabing(keywords, headers):
    base_url = 'https://habr.com'
    url = base_url + '/ru/all/'

    response = requests.get(url, headers=headers)
    text = response.text

    soup = bs4.BeautifulSoup(text, features='html.parser')
    articles = soup.find_all('article')

    for article in articles:
        art = re.split(r'\W+', article.text)
        for keyword in keywords:
            data__ = article.find(class_="tm-article-snippet__datetime-published").find("time").attrs["title"]
            title = article.find("h2").find("span").text
            href = article.find(class_="tm-article-snippet__title-link").attrs["href"]
            link = base_url + href
            if keyword in art:
                print(f'<дата> {data__} - <заголовок> - {title} - <ссылка> - {link}')
            else:
                response = requests.get(link, headers=HEADERS)
                text_ = response.text
                soup = bs4.BeautifulSoup(text_, features='html.parser')
                article_ = soup.find(id="post-content-body")
                art_ = re.split(r'\W+', article_.text)
                if keyword in art_:
                    print(f'<дата> {data__} - <заголовок> - {title} - <ссылка> - {link}')


if __name__ == "__main__":
    scrabing(KEYWORDS, HEADERS)
