import requests
from bs4 import BeautifulSoup as bs
import os


def requests_url(url):
    '''Функция делает запрос и возвращает html'''
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    return soup


def dict_catalog(url='https://wallpaperscraft.ru'):
    '''
    Функция достает имя категории,
    сайт и количество изображений из данной категории
    '''
    # Отправляет запрос на сайт
    # response = requests.get(url)
    # soup = bs(response.text, 'lxml')
    soup = requests_url(url)

    # Данные: имя категории и ссылка
    soup_find_catalog = soup.find(class_="menu__select").find_all()

    # Данные: Количество изображений
    soup_find_count = soup.find_all(class_='filter__count')

    # Категории изображений
    catalog = [
                  str(i).split()[-2]
                  for i in soup_find_catalog
              ][1:]
    # Ссылки на изображения
    link_catalog = [url + str(i).split()[-3].split('value="')[-1][:-2]
                    for i in soup_find_catalog
                    ][1:]

    count_catalog = [''.join(str(i).split('class="filter__count">')[-1].split('</span>')[:-1])
                     for i in soup_find_count
                     ]

    # Возвращаем список с которым будем работать Категория: (Ссылка, количество)
    return dict(zip(catalog, zip(link_catalog, count_catalog)))


def get_link_page(choice_user_catalog):
    """
    Функция возвращает последнюю страницу из категории
    """
    link_catalog = dict_catalog().get(choice_user_catalog)[0]
    soup_link_photo = requests_url(link_catalog)

    age_find_all = soup_link_photo.find_all('a', 'pager__link')

    link_page = [
        str(i_age).split()[2].replace('href="', '').replace('">2</a>', '').replace('">Последняя<span', '')
        for i_age in age_find_all
    ]

    # Последняя страница категории
    stop_link = int(link_page[-1].split('/')[-1].replace('page', ''))
    return stop_link, soup_link_photo, link_catalog


def requests_photo(url):
    return requests.get(url)


def save_photo(req, y, path):
    with open(f'{path}{y + 1}.jpg', 'wb') as file:
        file.write(req.content)


def work_content(choice_user_catalog, choice_user_age):
    link_general = 'https://wallpaperscraft.ru'
    if choice_user_catalog not in dict_catalog():
        print('Такой категории нет')
    else:
        stop_link, soup_link_photo, link_catalog = get_link_page(choice_user_catalog)
        if choice_user_age > stop_link:
            print(f'Вы преувеличили со страницами их всего {stop_link}')
        elif choice_user_age == 1:
            find_link_photo = str(
                    soup_link_photo.find('div', class_='content-main').find_all('a', class_='wallpapers__link')
                    ).split()

            link_photo = [
                    link_general + i_link.split('href="')[1].replace('">', '')
                    for i_link in find_link_photo if i_link.startswith('href="')
                    ]

            for y, i in enumerate(link_photo):
                get_i_soup = requests_url(i)
                get_part_page_one = str(
                    get_i_soup.find('div', class_='content-main').find_all(class_='wallpaper-table__cell')
                    ).split()
                get_part_one = ''.join(
                    [
                        link_general + i_link.split('href="')[1].replace('">', ',').split(',')[0]
                        for i_link in get_part_page_one if i_link.startswith('href="')
                    ]
                )

                get_new_link_soup = requests_url(get_part_one)
                get_url_photo_split = str(
                    get_new_link_soup.find('div', class_="gui-toolbar__item gui-hidden-mobile")
                    .find_all('a', class_="gui-button gui-button_full-height")).split('href="')

                url_photo = ''.join([o.split('">')[0] for o in get_url_photo_split if o.startswith('https')])
                download_photo_page_one = requests_photo(url_photo)
                with open(f'{"/home/masavnik/Рабочий стол/"}{y + 1}.jpg', 'wb') as file:
                    file.write(download_photo_page_one.content)

        else:
            soup_link_page = requests_url(f'{link_catalog}/page{choice_user_age}')
            find_link_photo1 = str(
                soup_link_page.find('div', class_='content-main').find_all('a', class_='wallpapers__link')
                ).split()

            link_photo_page = [
                link_general + i_link.split('href="')[1].replace('">', '')
                for i_link in find_link_photo1 if i_link.startswith('href="')
                ]

            for y_page, i_page in enumerate(link_photo_page):
                soup_1 = requests_url(i_page)

                get_part_link = str(
                    soup_1.find('div', class_='wallpaper-table').find_all(class_='wallpaper-table__cell')
                    ).split()[6]

                part_link = get_part_link.replace('href="', '').replace('</a>', '').split('"')[0]
                general_link_photo = link_general + part_link
                req_url = requests_url(general_link_photo)
                find_link = str(req_url.find_all('a', class_='JS-Popup', href=True)).split()

                link_photo = ''.join(
                    [
                        i.replace('href="', '').replace('">', '')
                        for i in find_link if i.startswith('href="')
                    ]
                )

                req_photo_page = requests_photo(link_photo)
                user_path = input('Вствте путь')
                save_photo(req_photo_page, y_page, user_path)



print('Выберите категорию:', ', '.join(dict_catalog().keys()))
user_catalog = input('Ввод: ')
print(f'Вы выбрали категорию {user_catalog}')
stop_link, soup_link_photo, link_catalog = get_link_page(user_catalog)
user_page = int(input(f'Выберете страницу, в категории {user_catalog} {stop_link} стр.'))
work_content(user_catalog, user_page)





