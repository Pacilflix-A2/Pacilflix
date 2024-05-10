from datetime import datetime

def convert_datetime_to_postgresql_format(datetime_str):
    list_time = datetime_str.split(" ")
    list_time[1] = list_time[1][0:len(list_time[1])-1]
    list_time[2] = list_time[2][0:len(list_time[2])-1]
    tanggal = ""
    print(list_time)
    tanggal += f"{list_time[2]}-"
    if list_time[0] == "January":
        tanggal += "01-"
    elif list_time[0] == "February":
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
    elif list_time[0] == "August":
        tanggal += "08-"
    elif list_time[0] == "September":
        tanggal += "09-"
    elif list_time[0] == "October":
        tanggal += "10-"
    elif list_time[0] == "November":
        tanggal += "11-"
    elif list_time[0] == "December":
        tanggal += "12-"
    if len(list_time[2]) == 1:
        tanggal += f"0{list_time[1]} "
    else:
        tanggal += list_time[1] +" "
    
    if list_time[4] == "a.m.":
        tanggal+=f"{list_time[3]}:00"
    else :
        if list_time[3].split(":")[0] == "12":
            tanggal+=f"{list_time[3]}:00"
        else:
            hour, minute = map(int, list_time[3].split(":"))
            hour = (hour + 12) % 24  # Convert to 24-hour format
            tanggal += f"{hour:02}:{minute:02}"

    return tanggal

# Example usage:
datetime_str = "Feb. 20, 2024, 8:06 a.m."
postgresql_datetime = convert_datetime_to_postgresql_format(datetime_str)
print(postgresql_datetime)  # Output: 2024-03-21 12:09:00
