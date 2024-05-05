from django.shortcuts import render
from django.db import connection

from query.query import *

def testing(request):
    fetched_data = query_sql('select username, asal_negara from pengguna')
    pengguna_list = [{'nama': row[0], 'asal_negara': row[1]} for row in fetched_data]
    context = {
        'pengguna_list': pengguna_list,
    }
    return render(request, "test.html", context)

def daftar_favorit(request):
    nama = 'hafizmuh'
    fetch_data = query_sql(f"select judul, timestamp from daftar_favorit where username = '{nama}'")
    daftar_favorit = [{'judul': row[0], 'timestamp': row[1]} for row in fetch_data]
    context = {
        'daftar_favorit': daftar_favorit,
    }
    return render(request, "daftar_favorit.html", context)


def daftar_unduhan(request):
    nama = 'hafizmuh'
    fetch_data = query_sql(f"select id_tayangan, timestamp from tayangan_terunduh where username = '{nama}'")
    print(fetch_data)
    daftar_unduhan = [{'judul': parse(query_sql(f"select judul from tayangan where id = '{row[0]}'")), 'timestamp': row[1]} for row in fetch_data]
    context = {
        'daftar_unduhan': daftar_unduhan,
    }
    return render(request, "daftar_unduhan.html", context)


