from requests import get, post, delete
from pprint import pprint

# тест на гет запрос
def printing_test_get(server):
    print('API GET METHOD TEST')
    pprint(get(f'{server}/api/events').json())  # корректный
    print()
    pprint(get(f'{server}/api/events/1').json())  # корретный
    print()
    pprint(get(f'{server}/api/events/99999999').json())  # некорректный
    print()
    pprint(get(f'{server}/api/events/q').json())  # неорректный
    print()

# тест на пост запрос
def printing_test_post(server):
    print('API POST METHOD TEST')
    pprint(post(f'{server}/api/events',
                json={'name': 'test', 'about': 'test_about', 'hall_id': 1}).json())  # корректный
    print()
    pprint(post(f'{server}/api/events', json={'title': 'title'}).json())  # некорректный
    print()
    pprint(post(f'{server}/api/events', json={}).json())  # некорректный

# тест на делете запрос
def printing_test_delete(server):
    print('API DELETE METHOD TEST')
    pprint(delete(f'{server}/api/events/999999').json())  # некорректный
    print()
    pprint(delete(f'{server}/api/events/18').json())  # корректный


printing_test_get('http://localhost:5000')
printing_test_post('http://localhost:5000')
printing_test_delete('http://localhost:5000')
