import re
import time
from collections import defaultdict

from bs4 import BeautifulSoup
import csv
import requests

BASE_URL = 'https://ru.wikipedia.org'
CATEGORY_URL = f'{BASE_URL}/wiki/Категория:Животные_по_алфавиту'
# CATEGORY_URL = f'{BASE_URL}/w/index.php?title=Категория:Животные_по_алфавиту&from=Юв'
# CATEGORY_URL = f'{BASE_URL}/w/index.php?title=Категория:Животные_по_алфавиту&from=Щв'


def get_page_soup(url: str) -> BeautifulSoup:
    """Получение объекта bs4."""

    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')


def is_russian(animal_name: str) -> bool:
    """Название животного на русском или нет."""

    return bool(re.search(pattern=r'^[а-яА-ЯёЁ]', string=animal_name))


def get_animals_on_page(soup: BeautifulSoup) -> list[str]:
    """Список всех животных на странице."""

    animals = []
    category_div = soup.find('div', id='mw-pages')

    if category_div:
        for li in category_div.find('div', class_='mw-category').find_all('li'):
            text = li.get_text().strip()
            if is_russian(text):
                animals.append(text)
    return animals


def get_next_page_url(base_url: str, soup: BeautifulSoup) -> str | None:
    """Получение ссылки на следующую страницу."""

    nav_div = soup.find('div', id='mw-pages')
    if nav_div:
        link = nav_div.find('a', string='Следующая страница')
        if link and link.get('href'):
            return f'{base_url}{link["href"]}'
    return None


def count_names_letters(animals: list[str]) -> defaultdict[str, int]:
    """Сбор статистики по буквам."""

    stats = defaultdict(int)
    for animal in animals:
        first_letter = animal[0].upper()
        stats[first_letter] += 1
    return stats


def export_counts_as_csv(counts: dict[str, int], file: str) -> None:
    """Запись статистики в CSV-файл."""

    with open(file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Буква', 'Количество'])
        writer.writerows(sorted(counts.items()))


def main():
    next_url = CATEGORY_URL
    animals = []

    while True:
        # В цикле будет получение url следующей страницы, а из неё будет взят список животных
        new_soup = get_page_soup(next_url)
        new_animals = get_animals_on_page(new_soup)
        animals.extend(new_animals)
        if not new_animals:
            print('Нет названий на русском — остановка.')
            break
        print(new_animals)

        next_url = get_next_page_url(base_url=BASE_URL, soup=new_soup)
        print('next url:', next_url)
        if not next_url:
            print('Следующей страницы нет.')
            break
        time.sleep(0.3)

    # Сбор и запись статистики в csv
    stat_count = count_names_letters(animals=animals)
    export_counts_as_csv(counts=stat_count, file='some.csv')


if __name__ == '__main__':
    main()
