
from datetime import datetime, timedelta
from devices.car.components.car.alerts import nearby_danger

DELTA = timedelta(0, 1*60)

nearby = []


def check(new):
    global nearby
    for i, car in enumerate(nearby):
        if datetime.now() - car['date'] < DELTA and car['carID'] == new['carID']:
            print 'removing nearby car: ' + nearby[i]
            nearby.pop(i)


def add(car):
    global nearby

    check(car)

    if car['state'] == 'danger':
        nearby_danger()

    print 'adding new nearby car'
    nearby.append({
        'carID'     : car['carID'],
        'location'  : car['location'],
        'date'      : datetime.now(),
    })
