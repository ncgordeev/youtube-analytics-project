import json
from config import YT_API_KEY

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    @classmethod
    def get_service(cls):
        youtube_api_obj = build('youtube', 'v3', developerKey=YT_API_KEY)
        return youtube_api_obj

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        current_channel = youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(current_channel, indent=2, ensure_ascii=False))


youtube = Channel.get_service()
