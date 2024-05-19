from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection

from general.query import *
from general.auth import *

def kontributor(request):
    if not is_authenticated(request):
        return render(request, '404.html')
    role_filter = request.GET.get('role', '')
    formatted_role_filter = role_filter.replace('_', ' ').title()

    if role_filter:
        sql_query = f"""
            SELECT c.id, c.nama, c.jenis_kelamin, c.kewarganegaraan, '{formatted_role_filter}' AS tipe
            FROM contributors c
            JOIN {role_filter} r ON c.id = r.id
        """
        rows = query_select(sql_query, ())
    else:
        sql_query = """
            SELECT c.id, c.nama, c.jenis_kelamin, c.kewarganegaraan, 
            CASE
                WHEN s.id IS NOT NULL THEN 'Sutradara'
                WHEN p.id IS NOT NULL THEN 'Pemain'
                WHEN ps.id IS NOT NULL THEN 'Penulis Skenario'
            END AS tipe
            FROM contributors c
            LEFT JOIN sutradara s ON c.id = s.id
            LEFT JOIN pemain p ON c.id = p.id
            LEFT JOIN penulis_skenario ps ON c.id = ps.id
        """
        rows = query_select(sql_query, ())
    

    contributors = [{
        'id': row[0],
        'nama': row[1],
        'jenis_kelamin': 'Laki-laki' if row[2] == 1 else 'Perempuan',
        'kewarganegaraan': row[3],
        'tipe': row[4]
    } for row in rows]

    context = {
        'contributors': contributors,
        'selected_role': formatted_role_filter 
    }

    return render(request, "kontributor.html", context)