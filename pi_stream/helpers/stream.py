from googleapiclient.discovery import build
from datetime import datetime


class Stream(object):

    def __init__(self, config, secrets):
        self.secrets = config
        self.config = secrets
        self.service = self.set_up_service(self.secrets.api_key)
        self.broadcast_id = self.set_up_broadcast(self.service)
        self.stream = self.set_up_stream(self.service, self.broadcast_id)

    def make_seculedStartTime():
        # example: 2022-12-30T00:00:00.000Z
        return datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    def set_up_service(self, api_key):
        return build('youtube', 'v3', developerKey=api_key)

    def set_up_broadcast(self, service):

        broadcast_snippet = {
            'title': self.config.title,
            'scheduledStartTime': '2022-12-30T00:00:00.000Z'
        }

        broadcast_insert_response = service.liveBroadcasts().insert(
            part='snippet,status',
            body={
                'snippet': broadcast_snippet,
                'status': {
                    'privacyStatus': 'private'
                }
            }
        ).execute()

        # Get the ID of the new live broadcast
        return broadcast_insert_response['id']


    def set_up_stream(self, service, broadcast_id):

        stream_snippet = {
            'title': 'My Live Stream'
        }

        stream_insert_response = service.liveStreams().insert(
            part='snippet,cdn',
            body={
                'snippet': stream_snippet,
                'cdn': {
                    'format': '1080p',
                    'ingestionType': 'rtmp'
                }
            }
        ).execute()

        # Get the ID of the new live stream
        stream_id = stream_insert_response['id']

        bind_broadcast_response = service.liveBroadcasts().bind(
            part='id,contentDetails',
            id=broadcast_id,
            streamId=stream_id
        ).execute()

