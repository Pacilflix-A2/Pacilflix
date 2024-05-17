from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from general.query import *
from general.auth import *

def kelola(request):
    if not is_authenticated(request):
        return render(request, '404.html')
    username = get_current_user(request)['username']
    # dukungan_perangkat = request.session.get('dukungan_perangkat')

    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT Transaction.nama_paket, Paket.harga, Paket.resolusi_layar, STRING_AGG(DUKUNGAN_PERANGKAT.dukungan_perangkat, ', ') AS devices, Transaction.start_date_time, Transaction.end_date_time, Transaction.metode_pembayaran, Transaction.timestamp_pembayaran
            FROM Transaction
            JOIN Paket ON Transaction.nama_paket = Paket.nama
            JOIN DUKUNGAN_PERANGKAT ON Paket.nama = DUKUNGAN_PERANGKAT.nama_paket
            WHERE Transaction.username = '{username}' AND Transaction.end_date_time >= CURRENT_DATE
            GROUP BY Transaction.nama_paket, Paket.harga, Paket.resolusi_layar, Transaction.start_date_time, Transaction.end_date_time, Transaction.metode_pembayaran, Transaction.timestamp_pembayaran
            ORDER BY Transaction.start_date_time DESC
            LIMIT 1
        """)
        active_subscription = [{'nama': row[0], 'harga': row[1], 'resolusi_layar': row[2], 'dukungan_perangkat': row[3], 'start_date_time': row[4], 'end_date_time': row[5], 'metode_pembayaran': row[6], 'timestamp_pembayaran': row[7]}
                               for row in cursor.fetchall()]
    # active_subscription = query_select(f"""
    #     SELECT Transaction.nama_paket, Paket.harga, Paket.resolusi_layar, DUKUNGAN_PERANGKAT.dukungan_perangkat, Transaction.start_date_time, Transaction.end_date_time, Transaction.metode_pembayaran, Transaction.timestamp_pembayaran
    #     FROM Transaction
    #     JOIN Paket ON Transaction.nama_paket = Paket.nama
    #     JOIN DUKUNGAN_PERANGKAT ON Paket.nama = DUKUNGAN_PERANGKAT.nama_paket
    #     WHERE Transaction.username = '{username}' AND Transaction.end_date_time >= CURRENT_DATE
    #     ORDER BY Transaction.start_date_time DESC
    #     LIMIT 1
    # """)

    # active_subscription = [{'nama': row[0], 'harga': row[1], 'resolusi_layar': row[2], 'dukungan_perangkat': dukungan_perangkat, 'start_date_time': row[4], 'end_date_time': row[5], 'metode_pembayaran': row[6], 'timestamp_pembayaran': row[7]}
    #                     for row in active_subscription]


    # available_packages = query_select("""
    #     SELECT Paket.nama, Paket.harga, Paket.resolusi_layar, STRING_AGG(DUKUNGAN_PERANGKAT.dukungan_perangkat, ', ') AS dukungan_perangkat
    #     FROM Paket
    #     JOIN DUKUNGAN_PERANGKAT ON Paket.nama = DUKUNGAN_PERANGKAT.nama_paket
    #     GROUP BY Paket.nama, Paket.harga, Paket.resolusi_layar
    # """)

    # available_packages = [{'nama': row[0], 'harga': row[1], 'resolusi_layar': row[2], 'dukungan_perangkat': row[3]}
    #                       for row in available_packages]

    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT Paket.nama, Paket.harga, Paket.resolusi_layar, STRING_AGG(DUKUNGAN_PERANGKAT.dukungan_perangkat, ', ')
            FROM Paket
            JOIN DUKUNGAN_PERANGKAT ON Paket.nama = DUKUNGAN_PERANGKAT.nama_paket
            GROUP BY Paket.nama, Paket.harga, Paket.resolusi_layar
            ORDER BY Paket.harga ASC
        """)

        available_packages = [{'nama': row[0], 'harga': row[1], 'resolusi_layar': row[2], 'dukungan_perangkat': row[3]}
                              for row in cursor.fetchall()]
        
    transaction_history = query_select(f"""
        SELECT T.nama_paket, T.start_date_time, T.end_date_time, T.metode_pembayaran, T.timestamp_pembayaran, P.harga
        FROM Transaction T
        JOIN Paket P ON T.nama_paket = P.nama
        WHERE T.username = '{username}'
        ORDER BY T.start_date_time DESC
    """)

    transaction_history = [{'nama_paket': row[0], 'start_date_time': row[1], 'end_date_time': row[2], 'metode_pembayaran': row[3], 'timestamp_pembayaran': row[4], 'total_pembayaran': row[5]}
                        for row in transaction_history]


    context = {
        'active_subscription': active_subscription,
        'available_packages': available_packages,
        'transaction_history': transaction_history,
    }
    return render(request, "kelola.html", context)

@csrf_exempt
def display_beli(request, nama_paket):
    if not is_authenticated(request):
        return render(request, '404.html')
    if request.method == 'POST':
        harga = request.POST.get('harga')
        resolusi_layar = request.POST.get('resolusi_layar')
        dukungan_perangkat = request.POST.get('dukungan_perangkat')

    paket_context = {
        'nama': nama_paket,
        'harga': harga,
        'resolusi_layar': resolusi_layar,
        'dukungan_perangkat': dukungan_perangkat
    }
    payment_methods = ['Transfer Bank', 'Kartu Kredit', 'E-Wallet']
    context = {
        'paket': paket_context,
        'payment_methods': payment_methods
    }
    return render(request, 'beli.html', context)

@csrf_exempt
def process_purchase(request):
    if not is_authenticated(request):
        return render(request, '404.html')
    if request.method == 'POST':
        username = get_current_user(request)['username']
        nama_paket = request.POST.get('nama_paket')
        dukungan_perangkat = request.POST.get('dukungan_perangkat')
        payment_method = request.POST.get('payment_method')

        current_timestamp = timezone.now() 
        start_date = current_timestamp 
        end_date = start_date + timezone.timedelta(days=30)

        existing_transaction = query_select(f"""
            SELECT timestamp_pembayaran
            FROM Transaction
            WHERE username = '{username}' AND end_date_time >= CURRENT_DATE
            ORDER BY timestamp_pembayaran DESC LIMIT 1
        """)

        if existing_transaction:
            update_query = f"""
                UPDATE Transaction
                SET end_date_time = '{end_date.isoformat()}',
                    nama_paket = '{nama_paket}',
                    metode_pembayaran = '{payment_method}',
                    timestamp_pembayaran = '{current_timestamp.isoformat()}'
                WHERE timestamp_pembayaran = '{existing_transaction[0][0]}'
            """
            print(update_query)
        else:
            insert_query = f"""
                INSERT INTO Transaction (username, nama_paket, start_date_time, end_date_time, metode_pembayaran, timestamp_pembayaran)
                VALUES ('{username}', '{nama_paket}', '{start_date.isoformat()}', '{end_date.isoformat()}', '{payment_method}', '{current_timestamp.isoformat()}')
            """
        
        add_query(update_query if existing_transaction else insert_query)
        
        # request.session['dukungan_perangkat'] = dukungan_perangkat

        return redirect('kelola')

