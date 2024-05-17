from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from django.db import connection

from general.query import *
from general.auth import *

def kelola(request):
    username = get_current_user(request)['username']

    active_subscription = query_select(f"""
        SELECT Paket.nama, Paket.harga, Paket.resolusi_layar, DUKUNGAN_PERANGKAT.dukungan_perangkat, Transaction.start_date_time, Transaction.end_date_time, Transaction.metode_pembayaran, Transaction.timestamp_pembayaran
        FROM Transaction
        JOIN Paket ON Transaction.nama_paket = Paket.nama
        JOIN DUKUNGAN_PERANGKAT ON Paket.nama = DUKUNGAN_PERANGKAT.nama_paket
        WHERE Transaction.username = '{username}' AND Transaction.end_date_time >= CURRENT_DATE
        ORDER BY Transaction.start_date_time DESC
        LIMIT 1
    """)
    active_subscription = [{'nama': row[0], 'harga': row[1], 'resolusi_layar': row[2], 'dukungan_perangkat': row[3], 'start_date_time': row[4], 'end_date_time': row[5], 'metode_pembayaran': row[6], 'timestamp_pembayaran': row[7]}
                           for row in active_subscription]

    available_packages = query_select("""
        SELECT Paket.nama, Paket.harga, Paket.resolusi_layar, DUKUNGAN_PERANGKAT.dukungan_perangkat
        FROM Paket
        JOIN DUKUNGAN_PERANGKAT ON Paket.nama = DUKUNGAN_PERANGKAT.nama_paket
    """)
    available_packages = [{'nama': row[0], 'harga': row[1], 'resolusi_layar': row[2], 'dukungan_perangkat': row[3]}
                          for row in available_packages]

    transaction_history = query_select(f"""
        SELECT nama_paket, start_date_time, end_date_time, metode_pembayaran, timestamp_pembayaran
        FROM Transaction
        WHERE username = '{username}'
        ORDER BY timestamp_pembayaran DESC
    """)
    transaction_history = [{'nama_paket': row[0], 'start_date_time': row[1], 'end_date_time': row[2], 'metode_pembayaran': row[3], 'timestamp_pembayaran': row[4]}
                           for row in transaction_history]

    context = {
        'active_subscription': active_subscription,
        'available_packages': available_packages,
        'transaction_history': transaction_history,
    }
    return render(request, "kelola.html", context)

def display_beli(request, nama_paket):
    paket_details = query_select(f"""
        SELECT nama, harga, resolusi_layar, dukungan_perangkat
        FROM Paket
        JOIN Dukungan_Perangkat ON Paket.nama = Dukungan_Perangkat.nama_paket
        WHERE Paket.nama = '{nama_paket}'
    """)

    if not paket_details:
        return render(request, '404.html') 

    paket_context = {
        'nama': paket_details[0][0],
        'harga': paket_details[0][1],
        'resolusi_layar': paket_details[0][2],
        'dukungan_perangkat': paket_details[0][3]
    }

    payment_methods = ['Transfer Bank', 'Kartu Kredit', 'E-Wallet']
    context = {
        'paket': paket_context,
        'payment_methods': payment_methods
    }
    return render(request, 'beli.html', context)

# @login_required
def process_purchase(request):
    if request.method == 'POST':
        nama_paket = request.POST.get('nama_paket') 
        payment_method = request.POST.get('payment_method')

        if not nama_paket or not payment_method:
            return redirect('kelola')

        username = get_current_user(request)['username']
        print(username)
        
        start_date = timezone.now()
        end_date = start_date + timezone.timedelta(days=30)
        
        query = """
            INSERT INTO Transaction (username, nama_paket, start_date_time, end_date_time, metode_pembayaran, timestamp_pembayaran)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        with connection.cursor() as cursor:
            cursor.execute(query, [username, nama_paket, start_date, end_date, payment_method, timezone.now()])
        
        return redirect('kelola')