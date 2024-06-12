from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def run(playwright, url):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto(url)
    page.wait_for_timeout(5000)  # Ожидание загрузки контента
    content = page.content()
    browser.close()
    return content

def get_soup_from_url(playwright, url):
    html = run(playwright, url)
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def get_game_info(game_div):
    # Извлечение ссылки на игру
    link_tag = game_div.find('a', class_='g-card-no-deco')
    game_link = link_tag['href'] if link_tag else None

    # Извлечение названия игры
    title_tag = game_div.find('div', class_='ellipsis-2-lines')
    game_title = title_tag.get_text(strip=True) if title_tag else None

    # Извлечение количества предложений
    offers_tag = game_div.find('div', class_='g-chip-counter dark')
    offers_count = offers_tag.get_text(strip=True) if offers_tag else None

    return {
        'link': game_link,
        'title': game_title,
        'offers': offers_count
    }

def scrape_all_pages(base_url, total_pages):
    games = []
    
    with sync_playwright() as playwright:
        for page_num in range(1, total_pages + 1):
            url = f"{base_url}?page={page_num}"
            soup = get_soup_from_url(playwright, url)
            game_divs = soup.find_all('div', class_='col-sm-4 col-md-3 col-12')

            for game_div in game_divs:
                game_info = get_game_info(game_div)
                games.append(game_info)

    return games

def main():
    base_url = "https://www.g2g.com/trending/game-coins"
    total_pages = 8  # Замените на общее количество страниц

    games = scrape_all_pages(base_url, total_pages)

    # Вывод информации
    for game in games:
        print(f"Ссылка на игру: https://www.g2g.com"{game['link']}")
        print(f"Название игры: {game['title']}")
        print(f"Количество предложений: {game['offers']}")
        print()

if __name__ == '__main__':
    main()
