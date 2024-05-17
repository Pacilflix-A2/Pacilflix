from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect

from general.query import *
from general.auth import *
from django.utils import timezone
from datetime import timedelta

# Create your views here.
def trailer(request):
    search_query = request.GET.get('search', '')

    if search_query:
        # Perform the search query
        films = query_select(f"SELECT judul, sinopsis, url_video_trailer, release_date_trailer FROM tayangan WHERE id IN (SELECT id_tayangan FROM film) AND judul ILIKE '%{search_query}%'")
        series = query_select(f"SELECT judul, sinopsis, url_video_trailer, release_date_trailer FROM tayangan WHERE id IN (SELECT id_tayangan FROM series) AND judul ILIKE '%{search_query}%'")
    else:
        # Fetch all films and series
        films = query_select("SELECT judul, sinopsis, url_video_trailer, release_date_trailer FROM tayangan WHERE id IN (SELECT id_tayangan FROM film)")
        series = query_select("SELECT judul, sinopsis, url_video_trailer, release_date_trailer FROM tayangan WHERE id IN (SELECT id_tayangan FROM series)")

    # Fetch top 10 tayangan based on total views in the last 7 days
    last_7_days = timezone.now().date() - timedelta(days=7)
    top_tayangan = query_select(f"""
        SELECT tayangan.id, tayangan.judul, tayangan.sinopsis_trailer, tayangan.url_video_trailer, tayangan.release_date_trailer, COUNT(riwayat_nonton.id_tayangan) AS total_views
        FROM tayangan
        LEFT JOIN riwayat_nonton ON tayangan.id = riwayat_nonton.id_tayangan AND riwayat_nonton.start_date_time >= '{last_7_days}'
        GROUP BY tayangan.id
        ORDER BY total_views DESC
        LIMIT 10
    """)

    context = {
        'films': films,
        'series': series,
        'search_query': search_query,
        'top_tayangan': top_tayangan,
    }

    return render(request, 'trailer/trailer.html', context)

def trailer_test(request):
    # for testing purposes only
    top_tayangan = [
        (1, 'Tayangan 1', 'Sinopsis 1', 'URL 1', '2023-05-17', 100),
        (2, 'Tayangan 2', 'Sinopsis 2', 'URL 2', '2023-05-16', 80),
        (3, 'Tayangan 3', 'Sinopsis 3', 'URL 3', '2023-05-15', 60),
        (4, 'Tayangan 4', 'Sinopsis 4', 'URL 4', '2023-05-19', 70),
    ]

    context = {
        'films': [],
        'series': [],
        'search_query': '',
        'top_tayangan': top_tayangan,
    }

    return render(request, 'trailer/trailer.html', context)