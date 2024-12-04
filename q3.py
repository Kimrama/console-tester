
def get_total_time(hi, mi, ho, mo):
    return (ho * 60 + mo) - (hi * 60 + mi)

cmd = input("")
data = list(map(int, cmd.split(" ")))
hour_in = data[0]
minute_in = data[1]
hour_out = data[2] 
minute_out = data[3]

total_time = get_total_time(hour_in, minute_in, hour_out, minute_out)
if total_time < 0 and not(7 <= hour_in <= 23) and not( 0 <= minute_in <= 60) and not(7 <= hour_out <= 23) and not( 0 <= minute_out <= 60) :
    print("error")
else:
    if total_time <= 15:
        cost = 0
    elif 15 < total_time <= 180:
        cost = (int(total_time+59) // 60) * 10
    elif 180 < total_time <= 360:
        cost = 30 + ((int(total_time+59) // 60) - 3) * 20
    elif total_time > 360:
        cost = 200
    print(cost)
