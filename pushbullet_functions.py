"""
wrapper for pushbullet functions
"""
from sqlalchemy.orm import Session
from pushbullet import Pushbullet
import pushbullet_messages as pbm
import datetime

class PushbulletFunctions:
    """wrapper for pushbullet functions"""
    def __init__(self) -> None:
        self.PB_API_KEY = pbm.API_KEY
        self.pb = Pushbullet(self.PB_API_KEY)
        self.current_date = datetime.date.today()

        # glass trash day
        # http://www.mairie-stjeandillac.fr/index.php/vivre-a-saint-jean-dillac/vos-dechets
        #       --> http://www.mairie-stjeandillac.fr/images/pdf/cdc/2024_CDC_SJI_Calendrier%20de%20collecte%202024-A5.pdf
        # get one day before that I out the trash 'la veille'
        self.glass_tash_dates = [
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

    # scheduled function from FAST API utils (no arguments allowed)
    def send_notification_by_pushbullet(self, db: Session) -> None:
        
        # 0. update self.current for the rest of the functions/methods
        self.current_date = datetime.date.today()

        ### glass trashday notification ###
        self.glass_tash_dates()

    def glass_trash_day_task(self):
        for date in self.glass_tash_dates:
            if date == self.current_date :
                self.pb.push_note('Home:', pbm.GLASS_TRASH_DAY)