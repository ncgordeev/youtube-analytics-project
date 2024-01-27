import json
import os

from googleapiclient.discovery import build


class Video:
    api_key: str = os.getenv('YT_API_KEY')

    def __init__(self, video_id):
        """Инициализация Video"""
        self.__video_id = video_id
        self.video_info()

    @property
    def video_id(self):
        """Геттер video_id"""
        return self.__video_id

    @classmethod
    def get_service(cls):
        """Возвращает объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=cls.api_key)

    def __str__(self):
        return f"{self.title}"

    def video_info(self):
        """Информация о видео"""
        video_response = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                          id=self.__video_id).execute()
        try:
            self.title: str = video_response['items'][0]['snippet']['title']
            self.video_description: str = video_response['items'][0]['snippet']['description']
            self.video_url: str = f"https://youtu.be/{self.__video_id}"
            self.view_count = int(video_response['items'][0]['statistics']['viewCount'])
            self.like_count = int(video_response['items'][0]['statistics']['likeCount'])
            self.comment_count = int(video_response['items'][0]['statistics']['commentCount'])
        except IndexError:
            self.title = None
            self.video_description = None
            self.video_url = None
            self.view_count = None
            self.like_count = None
            self.comment_count = None

    def to_json(self, file_path):
        """Создание словаря с информацией о видео
        и запись в json файл"""
        info_video = {
            "id": self.__video_id,
            "title": self.title,
            "description": self.video_description,
            "link": self.video_url,
            "view_count": self.view_count,
            "likeCount": self.like_count,
            "comment_count": self.comment_count,

        }

        with open(file_path, f"{'a' if os.path.exists(file_path) else 'w'}") as file_json:
            json.dump(info_video, file_json, indent=2, ensure_ascii=False)
            file_json.write('\n')


class PLVideo(Video):

    def __init__(self, video_id, playlist_id):
        """Инициализация PLVideo"""
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def to_json(self, file_path):
        """Создание словаря с информацией о видео
        и запись в json файл"""
        info_video = {
            "id": self.video_id,
            "title": self.title,
            "description": self.video_description,
            "link": self.video_url,
            "view_count": self.view_count,
            "likeCount": self.like_count,
            "comment_count": self.comment_count,
            "id_playlist": self.playlist_id

        }

        with open(file_path, f"{'a' if os.path.exists(file_path) else 'w'}") as file_json:
            json.dump(info_video, file_json, indent=2, ensure_ascii=False)
            file_json.write('\n')
