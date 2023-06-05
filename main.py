import requests
from bs4 import BeautifulSoup as bs
import os

link_general = 'https://wallpaperscraft.ru'


def requests_url(url):
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

# def get_link_page(choice_user_catalog):
#     """
#     Функция возвращает последнюю страницу из категории
#     """
#     link_catalog = dict_catalog().get(choice_user_catalog)[0]
#     get_link_catalog = requests.get(link_catalog)
#     soup_link_photo = bs(get_link_catalog.text, 'lxml')
#     age_find_all = soup_link_photo.find_all('a', 'pager__link')
#
#     link_page = [
#         str(i_age).split()[2].replace('href="', '').replace('">2</a>', '').replace('">Последняя<span', '')
#         for i_age in age_find_all
#     ]
#
#     # Последняя страница категории
#     stop_link = int(link_page[-1].split('/')[-1].replace('page', ''))
#     return stop_link


def work_content(choice_user_catalog, choice_user_age):
    link_general = 'https://wallpaperscraft.ru'

    if choice_user_catalog not in dict_catalog():
        print('Такой категории нет')
    else:
        link_catalog = dict_catalog().get(choice_user_catalog)[0]
        get_link_catalog = requests.get(link_catalog)
        soup_link_photo = bs(get_link_catalog.text, 'lxml')

        age_find_all = soup_link_photo.find_all('a', 'pager__link')

        # Ссылки на страницы
        link_page = [
            str(i_age).split()[2].replace('href="', '').replace('">2</a>', '').replace('">Последняя<span', '')
            for i_age in age_find_all
        ]

        # Последняя страница категории
        stop_link = int(link_page[-1].split('/')[-1].replace('page', ''))

        if choice_user_age > stop_link:
            a = f'Вы преувеличили со страницами их всего {stop_link}'
        elif choice_user_age == 1:
            find_link_photo = str(
                soup_link_photo.find('div', class_='content-main').find_all('a', class_='wallpapers__link')).split()
            link_photo = [
                             link_general + i_link.split('href="')[1].replace('">', '') for i_link in find_link_photo if
                             i_link.startswith('href="')
                         ][:3]

            for y, i in enumerate(link_photo):
                get_i = requests.get(i)
                get_i_soup = bs(get_i.text, 'lxml')
                f = str(get_i_soup.find('div', class_='content-main').find_all(class_='wallpaper-table__cell')).split()

                d = ''.join([
                    link_general + i_link.split('href="')[1].replace('">', ',').split(',')[0]
                    for i_link in f if i_link.startswith('href="')
                ])
                get_new_link = requests.get(d)
                get_new_link_soup = bs(get_new_link.text, 'lxml')
                p = str(get_new_link_soup.find('div', class_="gui-toolbar__item gui-hidden-mobile"). \
                    find_all('a', class_="gui-button gui-button_full-height")).split('href="')

                q = ''.join([o.split('">')[0] for o in p if o.startswith('https')])
                fr = requests.get(q)
                with open(f'{"/home/masavnik/Рабочий стол/"}{y + 1}.jpg', 'wb') as file:
                    file.write(fr.content)





        else:
            # o = f'/home/masavnik/Рабочий стол/{choice_user_catalog}'
            # oss = os.mkdir(o)
            get_link_page = requests.get(f'{link_catalog}/page{choice_user_age}')
            soup_link_page = bs(get_link_page.text, 'lxml')
            find_link_photo1 = str(
                soup_link_page.find('div', class_='content-main').
                find_all('a', class_='wallpapers__link')
            ).split()

            link_photo_page = [
                link_general + i_link.split('href="')[1].replace('">', '') for i_link in find_link_photo1 if
                i_link.startswith('href="')
            ]
            print(link_photo_page)

            for y_page, i_page in enumerate(link_photo_page):
                i_page_get = requests.get(i_page)
                soup_1 = bs(i_page_get.text, 'lxml')
                fi = str(soup_1.find('div', class_='wallpaper-table').find_all(class_='wallpaper-table__cell')).split()[
                    6]
                l = fi.replace('href="', '').replace('</a>', '').split('"')[0]
                d = link_general + l
                req = requests.get(d)
                g = bs(req.text, 'lxml')
                y = str(g.find_all('a', class_='JS-Popup', href=True)).split()
                r = ''.join([i.replace('href="', '').replace('">', '') for i in y if i.startswith('href="')])
                h = requests.get(r)

                # with open(f'{o}/{y_page + 1}.jpg', 'wb') as file:
                #     file.write(h.content)


work_content('Фэнтези', 1)
