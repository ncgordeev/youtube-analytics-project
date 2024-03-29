import json
from config import YT_API_KEY

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id
        self.current_channel = self.get_channel_data()
        self.set_attributes()

    def set_attributes(self) -> None:
        """Устанавливает атрибуты экземпляра."""
        snippet = self.current_channel["items"][0]["snippet"]
        statistics = self.current_channel["items"][0]["statistics"]

        self.title = snippet["title"]
        self.description = snippet["description"]
        self.url = f"https://www.youtube.com/channel/{self.__channel_id}"
        self.subscriber_count = statistics["subscriberCount"]
        self.video_count = statistics["videoCount"]
        self.view_count = statistics["viewCount"]

    @classmethod
    def get_service(cls):
        """
        Возвращает объект для работы с API
        """
        return build('youtube', 'v3', developerKey=YT_API_KEY)

    @property
    def channel_id(self) -> str:
        return self.__channel_id

    def get_channel_data(self):
        """Метод для получения данных о канале по API"""
        return self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.current_channel, indent=2, ensure_ascii=False))

    def to_json(self, file_path: str) -> None:
        """
        Метод для сохранения данных атрибутов экземпляра класса
        """
        saving_data = {
            "channel id": self.__channel_id,
            "title": self.title,
            "description": self.description,
            "url": self.url,
            "subscriber count": self.subscriber_count,
            "video count": self.video_count,
            "view count": self.view_count,
        }
        try:
            with open(file_path, "w") as file:
                json.dump(saving_data, file, indent=2, ensure_ascii=False)
                file.write("\n")
        except IOError as e:
            print(f"Ошибка при записи в файл: {e}")
