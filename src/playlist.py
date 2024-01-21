import datetime
import os

import isodate
from googleapiclient.discovery import build

from src.video import Video


class PlayList:
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, playlist_id: str) -> None:
        """Инициализация плейлиста"""
        self.__playlist_id = playlist_id
        self.playlist_info()

    @property
    def playlist_id(self) -> str:
        """Геттер возращающий id плейлиста"""
        return self.__playlist_id

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=cls.api_key)

    def playlist_info(self) -> None:
        # запрос на получение информации о плейлисте
        playlist_info = self.get_service().playlists().list(part='snippet,contentDetails',
                                                            id=self.__playlist_id,
                                                            maxResults=50).execute()

        self.title = playlist_info['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.__playlist_id}"

        # запрос на получение всех видео плейлиста
        playlist_videos = self.get_service().playlistItems().list(part='snippet,contentDetails',
                                                                  playlistId=self.__playlist_id,
                                                                  maxResults=50).execute()

        self.video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]

        # запрос на получение информации о видео из списка
        video_response = self.get_service().videos().list(part='contentDetails,statistics',
                                                          id=','.join(self.video_ids)).execute()
        full_time = datetime.timedelta()
        for video in video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            full_time += duration
        self.__total_duration = full_time

    @property
    def total_duration(self) -> str:
        """Возвращает общее время плейлиста"""
        return self.__total_duration

    def show_best_video(self) -> str:
        """Получение ссылки самого популярного видео"""
        max_likes = 0
        for video in self.video_ids:
            obj = Video(video)
            if obj.like_count > max_likes:
                max_likes = obj.like_count
                best_video = obj.video_url
        return best_video
