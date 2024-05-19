import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect


from general.query import *
from general.auth import *
from datetime import datetime, timezone

def datetime_convert(datetime_str):
    list_time = datetime_str.split(" ")
    list_time[1] = list_time[1][0:len(list_time[1])-1]
    list_time[2] = list_time[2][0:len(list_time[2])-1]
    tanggal = ""
    print(list_time)
    tanggal += f"{list_time[2]}-"
    if list_time[0] == "Jan.":
        tanggal += "01-"
    elif list_time[0] == "Feb.":
        tanggal += "02-"
    elif list_time[0] == "March":
        tanggal += "03-"
    elif list_time[0] == "April":
        tanggal += "04-"
    elif list_time[0] == "May":
        tanggal += "05-"
    elif list_time[0] == "June":
        tanggal += "06-"
    elif list_time[0] == "July":
        tanggal += "07-"
    elif list_time[0] == "Aug.":
        tanggal += "08-"
    elif list_time[0] == "Sep.":
        tanggal += "09-"
    elif list_time[0] == "Oct.":
        tanggal += "10-"
    elif list_time[0] == "Nov.":
        tanggal += "11-"
    elif list_time[0] == "Dec.":
        tanggal += "12-"
    if len(list_time[2]) == 1:
        tanggal += f"0{list_time[1]} "
    else:
        tanggal += list_time[1] +" "
    
    if list_time[4] == "a.m.":
        if list_time[3].split(":")[0] == "12":
            if len(list_time[3].split(":")) == 1:
                list_time[3] = "00"
            elif len(list_time[3].split(":")) == 2:
                list_time[3] = ":".join(["00", list_time[3].split(":")[1]])
            else :
                list_time[3] = ":".join(["00", list_time[3].split(":")[1], list_time[3].split(":")[2]])
        if ":" not in list_time[3]:
            tanggal += f"{list_time[3]}:00:"
        else :
            tanggal+=f"{list_time[3]}:"
    else :
        if ":" in list_time[3]:
            if list_time[3].split(":")[0] == "12":
                tanggal+=f"{list_time[3]}:" #keknya salah dah
            else:
                hour, minute = map(int, list_time[3].split(":"))
                hour = (hour + 12) % 24  # Convert to 24-hour format
                tanggal += f"{hour:02}:{minute:02}:"
        else :
            if list_time[3] == "12":
                tanggal += "12:00:"
            else :
                hour = (int(list_time[3]) + 12)%24
                tanggal += f"{hour}:00:"
    #convert jika jam cuma 11 jadi 23:00:00

    if len(tanggal.split(" ")[1].split(":")[0])  == 1 :
        tanggal1 = tanggal.split(" ")[0]
        tanggal2 = tanggal.split(" ")[1]
        tanggal = tanggal1 +" 0"+tanggal2

    return tanggal

def daftar_favorit(request):
    if not is_authenticated(request):
        return render(request, '404.html')
    nama = get_current_user(request)['username']
    fetch_data = query_select("select judul, timestamp from daftar_favorit where username = %s", [nama])
    daftar_favorit = [{'judul': row[0], 'timestamp': row[1]} for row in fetch_data]
    context = {
        'daftar_favorit': daftar_favorit,
    }
    return render(request, "daftar_favorit.html", context)


def daftar_unduhan(request):
    if not is_authenticated(request):
        return render(request, '404.html')
    nama = get_current_user(request)['username']
    fetch_data = query_select("select id_tayangan, timestamp from tayangan_terunduh where username = %s", [nama])
    daftar_unduhan = [{'judul': parse(query_select("select judul from tayangan where id = %s", [row[0]])), 'timestamp': row[1]} for row in fetch_data]
    context = {
        'daftar_unduhan': daftar_unduhan,
    }
    return render(request, "daftar_unduhan.html", context)

@csrf_exempt
def delete_downloaded_item(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        timestamp = request.POST.get('timestamp')

        try:
            id_tayangan = parse(query_select("select id from tayangan where judul = %s", [judul]))
            with connection.cursor() as cursor:
                print("delete from tayangan_terunduh where id_tayangan = %s and timestamp >= %s and timestamp <= %s", (id_tayangan, f"{datetime_convert(timestamp)}00", f"{datetime_convert(timestamp)}59"))
                cursor.execute("delete from tayangan_terunduh where id_tayangan = %s and timestamp >= %s and timestamp <= %s and username = %s", (id_tayangan, f"{datetime_convert(timestamp)}00", f"{datetime_convert(timestamp)}59", get_current_user(request)['username']))
                cursor.close()
                connection.close()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e).split("\n")[0]})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
@csrf_exempt
def delete_favorit_item(request):
    if request.method == 'POST':
        judul = request.POST.get('judul')
        timestamp = request.POST.get('timestamp')

        try:
            with connection.cursor() as cursor:
                print(f"delete from daftar_favorit where judul = '{judul}' and timestamp >= '{datetime_convert(timestamp)}00' and timestamp <= '{datetime_convert(timestamp)}59'")
                cursor.execute("delete from daftar_favorit where judul = %s and timestamp >= %s and timestamp <= %s and username = %s", (judul, f"{datetime_convert(timestamp)}00", f"{datetime_convert(timestamp)}59", get_current_user(request)['username']))
                cursor.close() 
                connection.close()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e).split("\n")[0]})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
def detail_favorit(request, judul, timestamp):
    if not is_authenticated(request):
        return render(request, '404.html')
    nama = get_current_user(request)['username']
    fetch_data = query_select("select id_tayangan from tayangan_memiliki_daftar_favorit where username = %s and  timestamp = %s", (nama, timestamp))
    daftar_tayangan = [{'judul': parse(query_select("select judul from tayangan where id = %s", [row[0]]))} for row in fetch_data]
    context = {
        'judul' : judul,
        'timestamp' : timestamp,
        'daftar_tayangan': daftar_tayangan,
    }
    return render(request, "detail_favorit.html", context)

@csrf_exempt
def delete_favorit_tayangan(request):
    if request.method == 'POST':
        judul = request.GET.get('judul')
        timestamp = request.GET.get('timestamp')
        try:
            id_tayangan = parse(query_select("select id from tayangan where judul = %s", [judul]))
            with connection.cursor() as cursor:
                cursor.execute("delete from tayangan_memiliki_daftar_favorit where id_tayangan = %s and timestamp = %s and username = %s", (id_tayangan, timestamp, get_current_user(request)['username']))
                cursor.close()
                connection.close()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e).split("\n")[0]})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})
    
@csrf_exempt
def tambah_favorit(request):
    if request.method == 'POST':
        favorite_title = request.POST.get('favoriteTitle')
        judul_tayangan = request.POST.get('judul_film')
        try:
            # Assuming you have a user associated with the request
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM tayangan WHERE judul = %s", [judul_tayangan])
                id_tay = cursor.fetchone()[0]
                cursor.execute("SELECT timestamp FROM daftar_favorit WHERE judul = %s", [favorite_title])
                timestamp = cursor.fetchone()[0]
                cursor.execute("INSERT INTO tayangan_memiliki_daftar_favorit VALUES (%s, %s, %s)", (id_tay, timestamp, get_current_user(request)['username']))
            return JsonResponse({'success': True})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False})
    return JsonResponse({'success': False})


@csrf_exempt
def unduh_tayangan(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        judul_film = data.get('judul_film')
        print(judul_film)
        current_timestamp = datetime.now() 
        print(current_timestamp)
        # Perform any necessary operations here, such as downloading the content
        with connection.cursor() as cursor:
            cursor.execute("SELECT id FROM tayangan WHERE judul = %s", [judul_film])
            id_tay = parse(cursor.fetchall())
            cursor.execute("insert into tayangan_terunduh values (%s, %s, %s)", (id_tay, get_current_user(request)['username'], current_timestamp.isoformat()))
        
        # Example response
        return JsonResponse({'success': True})
    
    # Handle GET requests or other methods
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)