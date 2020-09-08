from pyfcm import FCMNotification
from datetime import datetime


class NotificationService:
    emojis = ['😀', '😃', '😄']

    def __init__(self):
        self.push_service = FCMNotification(
            api_key='AAAACF33vmU:APA91bEbusaYFTevZojcCfM_h3Q9B4vc8PRegcL_AC0y9mBJqQsugkomUp7dO-iTRPqrpaAWAKrw5dO_gHiqhYotg11fBXLVkMmOycR8H2Uh3jaYgKMieZBlec-MLKopD-cCihchkrd1')

    def send_message(self, fcmToken, name, username):
        index = datetime.now().minute % 3
        message_title = username + ' is now following you!'
        message_body = 'Your latest posts will be visible to ' + username if name == None else name + ' ' + \
                                                                                               NotificationService.emojis[
                                                                                                   index]
        result = self.push_service.notify_single_device(registration_id=fcmToken, message_title=message_title,
                                                        message_body=message_body)
