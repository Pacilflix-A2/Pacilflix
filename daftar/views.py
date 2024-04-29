from django.shortcuts import render

# Create your views here.
def daftar_favorit(request):
    list_judul = [
        "Program", "Difficult", "Within", "Window", "Relationship", "Present", 
        "Street", "Same", "Station", "Sit", "Coach", "Chance", "Game", "Figure", 
        "Writer", "Nothing", "Guy", "Television", "Million", "Open", "Song", "Bill", 
        "Serve", "However", "Spring"
    ]
    
    list_time = [
        "2024-03-01 04:08:37", "2024-02-07 20:20:45", "2024-04-11 18:37:33", 
        "2024-02-05 06:32:47", "2024-04-17 02:11:07", "2024-01-15 16:40:57", 
        "2024-03-10 16:46:43", "2024-03-13 15:59:20", "2024-01-12 05:39:24", 
        "2024-02-04 01:27:16", "2024-03-12 18:56:50", "2024-01-24 01:40:53", 
        "2024-01-03 01:42:23", "2024-03-22 04:50:06", "2024-04-01 19:10:30", 
        "2024-02-06 16:23:28", "2024-02-17 16:35:09", "2024-04-01 02:35:06", 
        "2024-02-07 09:16:18", "2024-03-15 08:15:48", "2024-03-12 20:49:24", 
        "2024-02-11 05:17:58", "2024-04-09 21:24:28", "2024-02-22 00:51:50", 
        "2024-03-30 13:38:21"
    ]
    
    # Gabungkan kedua list menjadi satu list tuple
    daftar_favorit = zip(list_judul, list_time)
    
    context = {
        'daftar_favorit': daftar_favorit,
    }
    return render(request, "daftar_favorit.html", context)


def daftar_unduhan(request):
    list_judul = [
        "Program", "Difficult", "Within", "Window", "Relationship", "Present", 
        "Street", "Same", "Station", "Sit", "Coach", "Chance", "Game", "Figure", 
        "Writer", "Nothing", "Guy", "Television", "Million", "Open", "Song", "Bill", 
        "Serve", "However", "Spring"
    ]
    
    list_time = [
        "2024-03-01 04:08:37", "2024-02-07 20:20:45", "2024-04-11 18:37:33", 
        "2024-02-05 06:32:47", "2024-04-17 02:11:07", "2024-01-15 16:40:57", 
        "2024-03-10 16:46:43", "2024-03-13 15:59:20", "2024-01-12 05:39:24", 
        "2024-02-04 01:27:16", "2024-03-12 18:56:50", "2024-01-24 01:40:53", 
        "2024-01-03 01:42:23", "2024-03-22 04:50:06", "2024-04-01 19:10:30", 
        "2024-02-06 16:23:28", "2024-02-17 16:35:09", "2024-04-01 02:35:06", 
        "2024-02-07 09:16:18", "2024-03-15 08:15:48", "2024-03-12 20:49:24", 
        "2024-02-11 05:17:58", "2024-04-09 21:24:28", "2024-02-22 00:51:50", 
        "2024-03-30 13:38:21"
    ]
    
    # Gabungkan kedua list menjadi satu list tuple
    daftar_favorit = zip(list_judul, list_time)
    
    context = {
        'daftar_unduhan': daftar_favorit,
    }
    return render(request, "daftar_unduhan.html", context)
