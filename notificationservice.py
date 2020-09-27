from pyfcm import FCMNotification
from datetime import datetime


class NotificationService:
    emojis = ['😀', '😃', '😄']

    def __init__(self):
        self.push_service = FCMNotification(
            api_key='AAAACF33vmU:APA91bEyseN_arsvODwTTmSFclgT5u_RzeWF4YBvvrOGHklfeEIPbAPIDZu38t3mazcbOMSRvu-iATCeRFmaPLckhhbe3YFVbMlGzsIs-78CrpXG7eKWxxFS3AVtA6pNb1p3R2mT4Zou')

    def send_message(self, fcmToken, name, username):
        index = datetime.now().minute % 3
        message_title = username + ' is now following you!'
        message_body = 'Your latest posts will be visible to ' + username if name == None else name + ' ' + \
                                                                                               NotificationService.emojis[
                                                                                                   index]
        result = self.push_service.notify_single_device(registration_id=fcmToken, message_title=message_title,
                                                        message_body=message_body)

    def send_featured_message(self, fcmToken, title, content=''):
        message_title = 'Yippee, your post got featured!'
        if title is not None:
            message_body = 'Your post titled ' + title + ' is in the daily top 150, check it out now!'
        else:
            message_body = 'Your post ' + content[:40] + '... is in the daily top 150, check it out now!'
        result = self.push_service.notify_single_device(registration_id=fcmToken, message_title=message_title,
                                                        message_body=message_body)

    def send_featured_blog_message(self, fcmToken, title, thumbnail):
        result = self.push_service.notify_single_device(registration_id=fcmToken, message_title=message_title,
                                                        message_body=message_body)
