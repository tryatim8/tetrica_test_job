from collections import defaultdict
import csv
import os
import unittest
from bs4 import BeautifulSoup

from task2.solution import (
    get_page_soup,
    is_russian,
    get_animals_on_page,
    get_next_page_url,
    count_names_letters,
    export_counts_as_csv,
)


class TestSecondTask(unittest.TestCase):
    """Тест программы скраппинга русских названий животных википедии."""

    @classmethod
    def setUpClass(cls):
        cls.BASE_URL = 'https://ru.wikipedia.org'
        cls.CATEGORY_URL = f'{cls.BASE_URL}/wiki/Категория:Животные_по_алфавиту'

    def setUp(self):
        """Пример html для скраппинга животных и ссылки."""

        self.sample_html = '''
                <div id="mw-pages">
                    <div class="mw-category">
                        <ul>
                            <li><a href="/wiki/Белка">Белка</a></li>
                            <li><a href="/wiki/Волк">Волк</a></li>
                            <li><a href="/wiki/Siberian_tiger">Siberian tiger</a></li>
                        </ul>
                    </div>
                    <a href="/wiki/Категория:Животные_по_алфавиту?from=В" >Следующая страница</a>
                </div>
                '''
        self.soup = BeautifulSoup(self.sample_html, 'html.parser')
        self.filename = 'test_output.csv'

    def test_correct_get_page_soup(self):
        """Тест получения объекта bs4."""

        soup = get_page_soup(url=self.CATEGORY_URL)
        tags_and_classes = [
            ('body', 'mediawiki'),
            ('div', 'mw-body'),
            ('div', 'mw-body-content'),
            ('div', 'mw-category'),
        ]
        for tag, class_ in tags_and_classes:
            with self.subTest(value=tag):
                self.assertIsNotNone(
                    soup.find(tag, class_=class_),
                    msg=f'Не найден тег {tag} с классом {class_}',
                )

    def test_is_animal_russian(self):
        """Тест функции проверки русскоязычных названий."""

        name_is_russian = [
            ('Бурый медведь', True),
            ('Grizzly bear', False),
            ('', False),
            ('   Индийский слон', False),
            ('Беломорская beluga', True),
            ('52364786vbxncmvbj', False),
            ('$%^&*()_', False),
        ]

        for animal, result_bool in name_is_russian:
            with self.subTest():
                answer = 'на русском' if result_bool else 'не на русском'
                self.assertIs(
                    is_russian(animal_name=animal),
                    result_bool,
                    msg=f'Животное `{animal}` {answer}',
                )

    def test_get_animals_on_page(self):
        """Тест функции получения русских названий животных."""

        animals = get_animals_on_page(self.soup)
        expected = ['Белка', 'Волк']
        self.assertListEqual(animals, expected)

    def test_get_animals_on_page_no_div(self):
        """Тест получения пустого списка с пустой разметки."""

        soup_empty = BeautifulSoup('<div></div>', 'html.parser')
        animals = get_animals_on_page(soup_empty)
        self.assertEqual(animals, [])

    def test_get_next_page_url(self):
        """Тест получения ссылки из разметки."""

        url = get_next_page_url(base_url='https://ru.wikipedia.org', soup=self.soup)
        expected = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту?from=В'
        self.assertEqual(url, expected)

    def test_get_next_page_url_no_next(self):
        """Получение None вместо ссылки с пустой разметки."""

        html_no_next = '''
        <div id="mw-pages">
            <div class="mw-category"><ul></ul></div>
            <!-- Нет ссылки на следующую страницу -->
        </div>
        '''
        soup_no_next = BeautifulSoup(html_no_next, 'html.parser')
        url = get_next_page_url(base_url='https://ru.wikipedia.org', soup=soup_no_next)
        self.assertIsNone(url)

    def test_count_names_letters(self):
        """Тест подсчёта статистики по названиям."""

        animals = ['Белка', 'Волк', 'Волк', 'Антилопа']
        counts = count_names_letters(animals)
        expected = {'Б': 1, 'В': 2, 'А': 1}
        self.assertEqual(dict(counts), expected)

    def test_export_counts_as_csv(self):
        """Тест записи статистики в файл."""

        counts = {'А': 2, 'Б': 3}
        export_counts_as_csv(counts, self.filename)
        with self.subTest():
            self.assertTrue(os.path.exists(self.filename))

        with open(self.filename, encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        expected_rows = [
            ['Буква', 'Количество'],
            ['А', '2'],
            ['Б', '3'],
        ]
        self.assertEqual(rows, expected_rows)

        os.remove(self.filename)


if __name__ == '__main__':
    unittest.main()
