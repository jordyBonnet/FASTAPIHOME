"""
send pushbullet notification for glass trash day
"""
import datetime
import pushbullet_messages as pbm
from pushbullet import Pushbullet

GLASS_TRASH_DAY = "demain c'est le jour des poubelles verre"

# glass trash day
# http://www.mairie-stjeandillac.fr/index.php/vivre-a-saint-jean-dillac/vos-dechets
#       --> http://www.mairie-stjeandillac.fr/images/pdf/cdc/2024_CDC_SJI_Calendrier%20de%20collecte%202024-A5.pdf
# get one day before that I out the trash 'la veille'
glass_tash_dates = [
    datetime.datetime.strptime("16 Jan", "%d %b") - datetime.timedelta(days=1),
    datetime.datetime.strptime("20 Feb", "%d %b") - datetime.timedelta(days=1),
    datetime.datetime.strptime("19 Mar", "%d %b") - datetime.timedelta(days=1),
    datetime.datetime.strptime("16 Apr", "%d %b") - datetime.timedelta(days=1),
    datetime.datetime.strptime("21 May", "%d %b") - datetime.timedelta(days=1),
    datetime.datetime.strptime("18 Jun", "%d %b") - datetime.timedelta(days=1),
    datetime.datetime.strptime("16 Jul", "%d %b") - datetime.timedelta(days=1),
    datetime.datetime.strptime("20 Aug", "%d %b") - datetime.timedelta(days=1),
    datetime.datetime.strptime("17 Sep", "%d %b") - datetime.timedelta(days=1),
    datetime.datetime.strptime("15 Oct", "%d %b") - datetime.timedelta(days=1),
    datetime.datetime.strptime("19 Nov", "%d %b") - datetime.timedelta(days=1),
    datetime.datetime.strptime("17 Dec", "%d %b") - datetime.timedelta(days=1)
]

def send_message_to_user(message):
    pb = Pushbullet(pbm.API_KEY)
    pb.push_note("Home:", message)

def main():
    current_date = datetime.date.today()
    for date in glass_tash_dates:
        if date == current_date :
            send_message_to_user(GLASS_TRASH_DAY)