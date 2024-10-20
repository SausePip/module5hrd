import hashlib
import time

class User:
    def __init__(self, nickname: str, password: str, age: int):
        self.nickname = nickname
        self.password = self.hash_password(password)
        self.age = age

    @staticmethod
    def hash_password(password: str) -> int:
        return int(hashlib.sha256(password.encode()).hexdigest(), 16)

    def __str__(self):
        return self.nickname

    def __repr__(self):
        return f"User(nickname='{self.nickname}', password='***', age={self.age})"

    def __eq__(self, other):
        return isinstance(other, User) and self.nickname == other.nickname


class Video:
    def __init__(self, title: str, duration: int, adult_mode: bool = False):
        self.title = title
        self.duration = duration
        self.time_now = 0
        self.adult_mode = adult_mode

    def __str__(self):
        return f"Video(title='{self.title}', duration={self.duration}s, adult_mode={self.adult_mode})"

    def __repr__(self):
        return f"Video(title='{self.title}', duration={self.duration}, time_now={self.time_now}, adult_mode={self.adult_mode})"

    def __eq__(self, other):
        return isinstance(other, Video) and self.title == other.title

    def __contains__(self, search_word: str):
        return search_word.lower() in self.title.lower()


class UrTube:
    def __init__(self):
        self.users = []
        self.videos = []
        self.current_user = None

    def log_in(self, nickname: str, password: str):
        hashed_password = User.hash_password(password)
        for user in self.users:
            if user.nickname == nickname and user.password == hashed_password:
                self.current_user = user
                print(f"Пользователь {nickname} вошел в систему.")
                return
        print("Неверный логин или пароль.")

    def register(self, nickname: str, password: str, age: int):
        if any(user.nickname == nickname for user in self.users):
            print(f"Пользователь {nickname} уже существует.")
        else:
            new_user = User(nickname, password, age)
            self.users.append(new_user)
            self.current_user = new_user
            print(f"Пользователь {nickname} успешно зарегистрирован и вошел в систему.")

    def log_out(self):
        if self.current_user:
            print(f"Пользователь {self.current_user.nickname} вышел из системы.")
        self.current_user = None

    def add(self, *videos: Video):
        for video in videos:
            if video not in self.videos:
                self.videos.append(video)
                print(f"Видео '{video.title}' добавлено.")
            else:
                print(f"Видео с названием '{video.title}' уже существует.")

    def get_videos(self, search_word: str):
        return [video.title for video in self.videos if search_word in video]

    def watch_video(self, title: str):
        if not self.current_user:
            print("Войдите в аккаунт, чтобы смотреть видео.")
            return

        for video in self.videos:
            if video.title == title:
                if video.adult_mode and self.current_user.age < 18:
                    print("Вам нет 18 лет, пожалуйста покиньте страницу.")
                    return

                print(f"Начинается воспроизведение видео '{title}'...")
                for second in range(video.time_now, video.duration):
                    video.time_now = second
                    print(f"Просмотр {second + 1} секунда")
                    time.sleep(1)

                print("Конец видео")
                video.time_now = 0
                return

        print("Видео не найдено.")

    def __str__(self):
        return f"UrTube(current_user={self.current_user}, total_users={len(self.users)}, total_videos={len(self.videos)})"

    def __repr__(self):
        return f"UrTube(current_user={self.current_user!r}, users={self.users!r}, videos={self.videos!r})"


ur = UrTube()
v1 = Video('Лучший язык программирования 2024 года', 200)
v2 = Video('Для чего девушкам парень программист?', 10, adult_mode=True)

# Добавление видео
ur.add(v1, v2)

# Проверка поиска
print(ur.get_videos('лучший'))
print(ur.get_videos('ПРОГ'))

# Проверка на вход пользователя и возрастное ограничение
ur.watch_video('Для чего девушкам парень программист?')
ur.register('vasya_pupkin', 'lolkekcheburek', 13)
ur.watch_video('Для чего девушкам парень программист?')
ur.register('urban_pythonist', 'iScX4vIJClb9YQavjAgF', 25)
ur.watch_video('Для чего девушкам парень программист?')

# Проверка входа в другой аккаунт
ur.register('vasya_pupkin', 'F8098FM8fjm9jmi', 55)
print(ur.current_user)

# Попытка воспроизведения несуществующего видео
ur.watch_video('Лучший язык программирования 2024 года!')
