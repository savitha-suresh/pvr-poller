import requests
import logging
import os
import pywhatkit

logging.basicConfig(filename='ticket_poll', level=logging.DEBUG, format='%(asctime)s - : %(message)s')
logging.basicConfig(level=logging.INFO, )
logger = logging.getLogger()


def get_cinema_details(mid, name, date, city, lat, lng):
    
    url = "https://api2.pvrcinemas.com/PVRCinemasCMS/api/content/msessionsnew"

    payload = {
        'city': city,
        'lat': lat,
        'lng': lng,
        'av': '5.1',
        'pt': 'website',
        'mid': mid,
        'isSpi': 'YES',
        'date': date
    }
    response = requests.request("POST", url, data=payload)
    logger.info("Got response from pvr {} for {}".format(response.status_code, name))
    response.raise_for_status()
    res_json = response.json()
    if not res_json:
        return None
    logger.info("Message in response {}".format(res_json['msg']))
    return res_json.get('output', {}).get('cinemas', {})
    
def main():
    movie_list = [
        {
            "mid": 'NHO00021362',
            "name": "Oppn",
            "date": '2023-07-23' ,
            "city": 'Chennai',
            "lat": '12.972442',
            "lng": '77.580643',
        }, 

        {
            "mid": 'NHO00010763',
            "name": "Barbie",
            "date": '2023-07-23' ,
            "city": 'Chennai',
            "lat": '12.972442',
            "lng": '77.580643',
        }
        
    ]

    for movie in movie_list:
        cinema_details = get_cinema_details(**movie)
        if cinema_details:
            sathyam = any(cinema['cid'] == 1200 for cinema in cinema_details)
            if sathyam:
                logger.info("Sathyam opened for {}".format(movie["name"]))
                ph_number = os.environ.get('PH_NUM')
                text = "Sathyam openened for {}".format(movie["name"])
                pywhatkit.sendwhatmsg_instantly(ph_number, text,  5, True, 4)
                logger.info("Sent text {} to {}".format(text, ph_number))
            else:
                logger.info("Sathyam not opened for {}".format(movie["name"]))
                logger.info("cinemas opened - {}".format(len(cinema_details)))

if __name__ == "__main__":
    main()