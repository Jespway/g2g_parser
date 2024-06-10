from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup


def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.g2g.com/trending/game-coins")
    page.wait_for_timeout(5000)  # Ожидание загрузки контента
    content = page.content()
    browser.close()
    return content

    with sync_playwright() as playwright:
        html = run(playwright)
        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(html)

def get_soup():
    # Чтение сохраненного HTML-кода из файла
    with open('index.html', 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Создание объекта BeautifulSoup для парсинга HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Пример: Извлечение определенного блока контента по классу или идентификатору
    specific_div = soup.find_all('div', {'class': 'col-sm-4 col-md-3 col-12'})
    for div in specific_div:
        print(div)


def main():
    # soup = get_soup(url=url_themes)
    # themes = get_themes(soup=soup)
    
    # soup = get_soup(url='https://www.lego.com/en-us/themes/star-wars')
    # print(get_toys_pages(soup=soup))
    
    soup = get_soup()
    # get_toys_values(soup=soup)


if __name__== '__main__':
    main()