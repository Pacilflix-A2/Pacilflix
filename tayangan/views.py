from django.shortcuts import render

def tayangan_list(request):
    # Add logic to fetch tayangan data from the database
    # For now, you can use dummy data
    tayangan_data = [
        {'judul': 'Tayangan 1', 'sinopsis': 'Sinopsis tayangan 1', 'url': 'https://example.com/tayangan1', 'tanggal_rilis': '2023-06-01'},
        {'judul': 'Tayangan 2', 'sinopsis': 'Sinopsis tayangan 2', 'url': 'https://example.com/tayangan2', 'tanggal_rilis': '2023-06-02'},
        {'judul': 'Tayangan 3', 'sinopsis': 'Sinopsis tayangan 3', 'url': 'https://example.com/tayangan3', 'tanggal_rilis': '2023-06-03'},
        {'judul': 'Tayangan 4', 'sinopsis': 'Sinopsis tayangan 4', 'url': 'https://example.com/tayangan4', 'tanggal_rilis': '2023-06-04'},
        {'judul': 'Tayangan 5', 'sinopsis': 'Sinopsis tayangan 5', 'url': 'https://example.com/tayangan5', 'tanggal_rilis': '2023-06-05'},
    ]

    return render(request, 'tayangan/tayangan.html', {'tayangan_list': tayangan_data})

def hasil_pencarian(request):
    # Add logic to fetch search results from the database
    # For now, you can use dummy data
    search_results = [
        {'judul': 'Tayangan 1', 'sinopsis': 'Sinopsis tayangan 1', 'url': 'https://example.com/tayangan1', 'tanggal_rilis': '2023-06-01'},
        {'judul': 'Tayangan 2', 'sinopsis': 'Sinopsis tayangan 2', 'url': 'https://example.com/tayangan2', 'tanggal_rilis': '2023-06-02'},
    ]

    return render(request, 'tayangan/hasil_pencarian.html', {'search_results': search_results})

def detail_tayangan_film(request):
    film_data = {
        'judul': 'Gran Turismo',
        'genre': ['Action', 'Drama', 'Sci-fi'],
        'total_view': 12345,
        'rating_rata_rata': 9,
        'sinopsis': 'Lorem ipsum',
        'durasi_film': '2 Jam',
        'tanggal_rilis': '2020-10-10',
        'url_film': 'https://example.com/tayangan1',
        'asal_negara': 'Uzbekistan',
        'pemain': ['Andi', 'Budi'],
        'penulis_skenario': ['Jamal', 'Agung'],
        'sutradara': 'Mikail',
    }

    return render(request, 'tayangan/halaman_film.html', {'film_data': film_data})

def detail_tayangan_series(request):
    series_data = {
        'judul': 'Gran Turismo',
        'genre': ['Action', 'Drama', 'Sci-fi'],
        'total_view': 12345,
        'rating_rata_rata': 9,
        'sinopsis': 'Lorem ipsum',
        'durasi_film': '2 Jam',
        'tanggal_rilis': '2020-10-10',
        'url_film': 'https://example.com/tayangan1',
        'asal_negara': 'Uzbekistan',
        'pemain': ['Andi', 'Budi'],
        'penulis_skenario': ['Jamal', 'Agung'],
        'sutradara': 'Mikail',
    }

    return render(request, 'tayangan/halaman_series.html', {'series_data': series_data})

def detail_tayangan_episode(request):
    episode_data = {
        'judul': 'Gran Turismo',
        'genre': ['Action', 'Drama', 'Sci-fi'],
        'total_view': 12345,
        'rating_rata_rata': 9,
        'sinopsis': 'Lorem ipsum',
        'durasi_film': '2 Jam',
        'tanggal_rilis': '2020-10-10',
        'url_film': 'https://example.com/tayangan1',
        'asal_negara': 'Uzbekistan',
        'pemain': ['Andi', 'Budi'],
        'penulis_skenario': ['Jamal', 'Agung'],
        'sutradara': 'Mikail',
    }

    return render(request, 'tayangan/halaman_episode.html', {'episode_data': episode_data})