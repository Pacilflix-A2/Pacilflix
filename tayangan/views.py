from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from general.query import *
from general.auth import *
from django.utils import timezone
from datetime import timedelta

def tayangan_list(request):
    if not is_authenticated(request):
        return render(request, 'tayangan/404.html')
    
    search_query = request.GET.get('search', '')

    if search_query:
        # Perform the search query
        films = query_select("SELECT tayangan.id, tayangan.judul, tayangan.sinopsis, tayangan.url_video_trailer, tayangan.release_date_trailer FROM tayangan WHERE id IN (SELECT id_tayangan FROM film) AND judul ILIKE %s", ('%' + search_query + '%',))
        series = query_select("SELECT tayangan.id, tayangan.judul, tayangan.sinopsis, tayangan.url_video_trailer, tayangan.release_date_trailer FROM tayangan WHERE id IN (SELECT id_tayangan FROM series) AND judul ILIKE %s", ('%' + search_query + '%',))
    else:
        # Fetch all films and series
        films = query_select("SELECT tayangan.id, tayangan.judul, tayangan.sinopsis, tayangan.url_video_trailer, tayangan.release_date_trailer FROM tayangan WHERE id IN (SELECT id_tayangan FROM film)", ())
        series = query_select("SELECT tayangan.id, tayangan.judul, tayangan.sinopsis, tayangan.url_video_trailer, tayangan.release_date_trailer FROM tayangan WHERE id IN (SELECT id_tayangan FROM series)", ())

    # Fetch top 10 tayangan based on total views in the last 7 days
    last_7_days = timezone.now().date() - timedelta(days=7)
    top_tayangan = query_select("""
        SELECT 
            tayangan.id, 
            tayangan.judul, 
            tayangan.sinopsis_trailer, 
            tayangan.url_video_trailer, 
            tayangan.release_date_trailer, 
            COUNT(riwayat_nonton.id_tayangan) AS total_views,
            CASE 
                WHEN EXISTS (SELECT 1 FROM film WHERE film.id_tayangan = tayangan.id) THEN 'film'
                WHEN EXISTS (SELECT 1 FROM series WHERE series.id_tayangan = tayangan.id) THEN 'series'
            END AS type
        FROM tayangan
        LEFT JOIN riwayat_nonton ON tayangan.id = riwayat_nonton.id_tayangan AND riwayat_nonton.start_date_time >= %s
        GROUP BY tayangan.id
        ORDER BY total_views DESC
        LIMIT 10
    """, (last_7_days,))

    context = {
        'films': films,
        'series': series,
        'search_query': search_query,
        'top_tayangan': top_tayangan,
    }

    return render(request, 'tayangan/tayangan.html', context)

def detail_tayangan_film(request, film_id):
    if not is_authenticated(request):
        return render(request, 'tayangan/404.html')

    film = query_select("""
        SELECT 
            tayangan.judul, 
            tayangan.sinopsis, 
            tayangan.asal_negara, 
            film.url_video_film, 
            film.release_date_film, 
            film.durasi_film,
            (SELECT COUNT(*) FROM riwayat_nonton WHERE id_tayangan = %s) AS total_view,
            (SELECT AVG(rating) FROM ulasan WHERE id_tayangan = %s) AS rating_rata_rata,
            (SELECT STRING_AGG(genre, ', ') FROM genre_tayangan WHERE id_tayangan = %s) AS genre,
            (SELECT STRING_AGG(contributors.nama, ', ') FROM pemain 
                INNER JOIN contributors ON pemain.id = contributors.id
                INNER JOIN memainkan_tayangan ON pemain.id = memainkan_tayangan.id_pemain
                WHERE memainkan_tayangan.id_tayangan = %s) AS pemain,
            (SELECT STRING_AGG(contributors.nama, ', ') FROM penulis_skenario
                INNER JOIN contributors ON penulis_skenario.id = contributors.id
                INNER JOIN menulis_skenario_tayangan ON penulis_skenario.id = menulis_skenario_tayangan.id_penulis_skenario
                WHERE menulis_skenario_tayangan.id_tayangan = %s) AS penulis_skenario,
            (SELECT contributors.nama FROM sutradara
                INNER JOIN contributors ON sutradara.id = contributors.id
                WHERE sutradara.id = tayangan.id_sutradara) AS sutradara,
            CASE
                WHEN film.release_date_film <= NOW()::date THEN 'released'
                ELSE 'unreleased'
            END AS release_status
        FROM tayangan
        INNER JOIN film ON tayangan.id = film.id_tayangan
        WHERE tayangan.id = %s
    """, (film_id, film_id, film_id, film_id, film_id, film_id))

    if not film:
        return render(request, 'tayangan/404.html')

    film = film[0]

    reviews = query_select("""
        SELECT username, rating, deskripsi
        FROM ulasan
        WHERE id_tayangan = %s
        ORDER BY timestamp DESC
    """, (film_id,))

    context = {
        'film': film,
        'film_id': film_id,
        'reviews': reviews,
    }

    return render(request, 'tayangan/halaman_film.html', context)

def detail_tayangan_series(request, series_id):
    if not is_authenticated(request):
        return render(request, 'tayangan/404.html')

    series = query_select("""
        SELECT 
            tayangan.judul, 
            tayangan.sinopsis, 
            tayangan.asal_negara, 
            (SELECT COUNT(*) FROM riwayat_nonton WHERE id_tayangan = %s) AS total_view,
            (SELECT AVG(rating) FROM ulasan WHERE id_tayangan = %s) AS rating_rata_rata,
            (SELECT STRING_AGG(genre, ', ') FROM genre_tayangan WHERE id_tayangan = %s) AS genre,
            (SELECT STRING_AGG(contributors.nama, ', ') FROM pemain 
                INNER JOIN contributors ON pemain.id = contributors.id
                INNER JOIN memainkan_tayangan ON pemain.id = memainkan_tayangan.id_pemain
                WHERE memainkan_tayangan.id_tayangan = %s) AS pemain,
            (SELECT STRING_AGG(contributors.nama, ', ') FROM penulis_skenario
                INNER JOIN contributors ON penulis_skenario.id = contributors.id
                INNER JOIN menulis_skenario_tayangan ON penulis_skenario.id = menulis_skenario_tayangan.id_penulis_skenario
                WHERE menulis_skenario_tayangan.id_tayangan = %s) AS penulis_skenario,
            (SELECT contributors.nama FROM sutradara
                INNER JOIN contributors ON sutradara.id = contributors.id
                WHERE sutradara.id = tayangan.id_sutradara) AS sutradara
        FROM tayangan
        INNER JOIN series ON tayangan.id = series.id_tayangan
        WHERE tayangan.id = %s
    """, (series_id, series_id, series_id, series_id, series_id, series_id))

    if not series:
        return render(request, 'tayangan/404.html')

    series = series[0]

    episodes = query_select("""
        SELECT 
            episode.sub_judul,
            episode.id_series
        FROM episode
        WHERE episode.id_series = %s
        ORDER BY episode.release_date
    """, (series_id,))

    reviews = query_select("""
        SELECT username, rating, deskripsi
        FROM ulasan
        WHERE id_tayangan = %s
        ORDER BY timestamp DESC
    """, (series_id,))

    context = {
        'series': series,
        'episodes': episodes,
        'reviews': reviews,
        'series_id': series_id,
    }

    return render(request, 'tayangan/halaman_series.html', context)

def detail_tayangan_episode(request, episode_id):
    if not is_authenticated(request):
        return render(request, 'tayangan/404.html')
    
    sub_judul = request.GET.get('sub_judul')

    episode = query_select("""
        SELECT
            tayangan.judul,
            episode.sub_judul,
            episode.sinopsis,
            episode.durasi,
            episode.url_video,
            episode.release_date,
            CASE
                WHEN episode.release_date <= NOW()::date THEN 'released'
                ELSE 'unreleased'
            END AS release_status
        FROM episode
        INNER JOIN series ON episode.id_series = series.id_tayangan
        INNER JOIN tayangan ON series.id_tayangan = tayangan.id
        WHERE episode.id_series = %s AND episode.sub_judul = %s
    """, (episode_id, sub_judul))

    if not episode:
        return render(request, 'tayangan/404.html')

    episode = episode[0]

    other_episodes = query_select("""
        SELECT
            episode.sub_judul,
            episode.id_series
        FROM episode
        WHERE episode.id_series = %s AND episode.sub_judul != %s
        ORDER BY episode.release_date
    """, (episode_id, sub_judul))

    context = {
        'episode': episode,
        'other_episodes': other_episodes,
        'series_id': episode_id,
    }

    return render(request, 'tayangan/halaman_episode.html', context)

@csrf_exempt
def record_film_watch(request, film_id):
    if request.method == 'POST':
        username = get_current_user(request)['username']

        # Get the film's duration
        film_duration = query_select("""
            SELECT durasi_film
            FROM film
            WHERE id_tayangan = %s
        """, (film_id,))[0][0]

        # Calculate the start_date_time based on the end_date_time and film's duration
        query = """
            INSERT INTO RIWAYAT_NONTON (id_tayangan, username, start_date_time, end_date_time)
            VALUES (
                %s,
                %s,
                NOW() - INTERVAL '%s minutes',
                NOW()
            )
        """
        add_query(query, (film_id, username, film_duration))
        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)

@csrf_exempt
def record_series_watch(request, series_id):
    if request.method == 'POST':
        username = get_current_user(request)['username']

        # Get the episode's duration
        episode_duration = query_select("""
            SELECT durasi
            FROM episode
            WHERE id_series = %s
            ORDER BY release_date DESC
            LIMIT 1
        """, (series_id,))[0][0]

        # Calculate the start_date_time based on the end_date_time and episode's duration
        query = """
            INSERT INTO RIWAYAT_NONTON (id_tayangan, username, start_date_time, end_date_time)
            VALUES (
                %s,
                %s,
                NOW() - INTERVAL '%s minutes',
                NOW()
            )
        """
        add_query(query, (series_id, username, episode_duration))
        return JsonResponse({'success': True})

    return JsonResponse({'success': False}, status=400)

@csrf_exempt
def submit_review(request, tayangan_id):
    if request.method == 'POST':
        username = get_current_user(request)['username']
        deskripsi = request.POST.get('deskripsi')
        rating = request.POST.get('rating')

        try:
            query = """
                INSERT INTO ulasan (id_tayangan, username, timestamp, rating, deskripsi)
                VALUES (%s, %s, NOW(), %s, %s)
            """
            params = (tayangan_id, username, rating, deskripsi)
            add_query(query, params)
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})