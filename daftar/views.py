from django.shortcuts import render
from django.db import connection

from query.query import *
from query.auth import *

def daftar_favorit(request):
    nama = get_current_user(request)['username']
    fetch_data = query_sql(f"select judul, timestamp from daftar_favorit where username = '{nama}'")
    daftar_favorit = [{'judul': row[0], 'timestamp': row[1]} for row in fetch_data]
    context = {
        'daftar_favorit': daftar_favorit,
    }
    return render(request, "daftar_favorit.html", context)


def daftar_unduhan(request):
    nama = get_current_user(request)['username']
    fetch_data = query_sql(f"select id_tayangan, timestamp from tayangan_terunduh where username = '{nama}'")
    daftar_unduhan = [{'judul': parse(query_sql(f"select judul from tayangan where id = '{row[0]}'")), 'timestamp': row[1]} for row in fetch_data]
    context = {
        'daftar_unduhan': daftar_unduhan,
    }
    return render(request, "daftar_unduhan.html", context)


