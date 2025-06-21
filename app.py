import requests
from flask import Flask, render_template, request
import time

app = Flask(__name__)

def get_top_anime(page=1, limit=25):
    '''Получает топ аниме по рейтингу'''
    try:
        url = f'https://api.jikan.moe/v4/top/anime'
        params = {
            'page': page,
            'limit': limit
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return {
                'anime_list': data['data'],
                'pagination': data.get('pagination', {}),
                'success': True
            }
        else:
            return {'success': False, 'error': f'Api error: {response.status_code}'}
    except Exception as e:
        return {'success': False, 'error': str(e)}
    
def get_anime_by_type(anime_type='tv', page=1):
    '''Получает топ аниме по типу (tv, movie, ova, special)'''
    try:
        url = f'https://api.jikan.moe/v4/top/anime'
        params = {
            'type': anime_type,
            'page': page,
            'limit': 25
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return {
                'anime_list': data['data'],
                'pagination': data.get('pagination', {}),
                'success': True,
                'type': anime_type
            }
        else:
            return {'success': False, 'error': f'Api error: {response.status_code}'}
    
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/')
def top_anime():
    '''Главная страница с топ аниме'''
    page = request.args.get('page', 1, type=int)
    anime_type = request.args.get('type', 'tv')

    if page < 1:
        page = 1
    elif page > 100:
        page = 100

    print(f'Загружаем топ {anime_type} аниме, страница {page}...')

    if anime_type == 'all':
        result = get_top_anime(page=page)
    else:
        result = get_anime_by_type(anime_type=anime_type, page=page)
    
    if not result['success']:
        return f'Ошибка загрузки данных: {result["error"]}', 500
    
    for i, anime in enumerate(result['anime_list']):
        anime['position'] = (page - 1) * 25 + i + 1
    
     # Типы аниме для фильтра
    anime_types = [
        {'value': 'all', 'name': 'Все'},
        {'value': 'tv', 'name': 'TV Сериалы'},
        {'value': 'movie', 'name': 'Фильмы'},
        {'value': 'ova', 'name': 'OVA'},
        {'value': 'special', 'name': 'Спешлы'},
        {'value': 'ona', 'name': 'ONA'},
        {'value': 'music', 'name': 'Музыка'}
    ]

    template_data = {
        'anime_list': result['anime_list'],
        'pagination': result.get('pagination', {}),
        'current_page': page,
        'current_type': anime_type,
        'anime_types': anime_types,
        'total_pages': min(result.get('pagination', {}).get('last_visivle_page', 1), 100)
    }

    return render_template('top_anime.html', data=template_data)