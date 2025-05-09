from moviepy.editor import VideoFileClip
import os
import pandas as pd
from abc import ABC, abstractmethod
import cv2


class Media(ABC):
    @abstractmethod
    def select_media(self):
        pass

    @abstractmethod
    def display_contents(self):
        pass


class Anime(Media):
    def __init__(self, anime_database):
        self.anime_database = anime_database

    def select_media(self):
        print("Select anime")
        self.watch_anime()

    def display_contents(self):
        pass

    def watch_anime(self):
        print("Choose an option:")
        print("1. View Anime List")
        print("2. Search Anime")
        option = input("Enter your choice (1/2): ")
        if option == "1":
            self.view_anime_list()
        elif option == "2":
            self.search_anime()
        else:
            print("Invalid choice.")

    def view_anime_list(self):
        print("Available Anime:")
        for anime_title in self.anime_database:
            print(f"- {anime_title.capitalize()}")
        anime_title = input("Enter anime title: ").lower()
        if anime_title in self.anime_database:
            self.display_anime_episodes(anime_title)
        else:
            print("Anime not found.")

    def display_anime_episodes(self, anime_title):
        print(f"Episodes of {anime_title.capitalize()}:")
        for i, episode in enumerate(self.anime_database[anime_title]["episodes"], start=1):
            print(f"{i}. {episode}")
        try:
            episode_number = int(input("Enter episode number: "))
            if 1 <= episode_number <= len(self.anime_database[anime_title]["episodes"]):
                video_path = self.anime_database[anime_title]["video_paths"][episode_number - 1]
                self.play_video(video_path)
            else:
                print("Invalid episode number.")
        except ValueError:
            print("Please enter a valid number.")

    def search_anime(self):
        search_query = input("Enter the name of the anime you're looking for: ").lower()
        found = False
        for anime_title in self.anime_database:
            if search_query in anime_title:
                print(f"Found matching anime: {anime_title.capitalize()}")
                found = True
        if not found:
            print("No matching anime found.")
    
    def play_video(self, video_path):
        try:
            video_clip = VideoFileClip(video_path)
            video_clip.preview()
        except Exception as e:
            print(f"Error playing video: {e}")


class Manga(Media):
    def __init__(self, manga_database):
        self.manga_database = manga_database

    def select_media(self):
        print("Select manga")
        self.read_manga()

    def display_contents(self):
        pass

    def read_manga(self):
        print("Choose a manga:")
        for i, manga_title in enumerate(self.manga_database, start=1):
            print(f"{i}. {manga_title.capitalize()}")
        manga_choice = int(input("Enter your choice: "))
        manga_title = list(self.manga_database.keys())[manga_choice - 1]
        self.display_manga_chapters(manga_title)

    def display_manga_chapters(self, manga_title):
        print(f"{manga_title.capitalize()} chapters:")
        for i, chapter in enumerate(self.manga_database[manga_title]["chapters"], start=1):
            print(f"{i}. {chapter}")
        chapter_number = int(input("Enter chapter number: "))
        manga_folder = self.manga_database[manga_title]["image_folder"]
        chapter_folder = os.path.join(manga_folder, f"Chapter_{chapter_number}")
        self.display_slideshow(chapter_folder)

    def display_slideshow(self, folder_path):
        image_files = sorted([
            f for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))
        ])
        for image_file in image_files:
            image_path = os.path.join(folder_path, image_file)
            image = cv2.imread(image_path)
            if image is not None:
                cv2.imshow('Manga Slideshow', image)
                if cv2.waitKey(0) & 0xFF == ord('q'):
                    break
        cv2.destroyAllWindows()


class MugiwaraTV:
    def __init__(self):
        self.anime_database = {
            "one piece": {
                "episodes": ["Luffy Gear 5th", "Luffy vs Lucci Gear 5th", "Zoro vs King", "Sanji vs Queen", "Shanks Haki"],
                "video_paths": [
                    "luffy gear 5th kaminami.mp4",
                    "luffy vs lucci gear 5th.mp4",
                    "Zoro vs King.mp4",
                    "SANJI VS QUEEN.mp4",
                    "Shanks haki.mp4"
                ]
            },
            "demon slayer": {
                "episodes": ["Episode 1", "Episode 2", "Episode 3"],
                "video_paths": [
                    "Demon Slayer Episode 1.mp4",
                    "Demon Slayer Episode 2.mp4",
                    "Demon Slayer Episode 3.mp4"
                ]
            },
            "ninja kamui": {
                "episodes": ["Episode 1", "Episode 2", "Episode 3"],
                "video_paths": [
                    "Ninja Kamui Episode 1.mp4",
                    "Ninja Kamui Episode 2.mp4",
                    "Ninja Kamui Episode 3.mp4"
                ]
            },
            "jujutsu kaisen": {
                "episodes": ["Episode 1", "Episode 2", "Episode 3"],
                "video_paths": [
                    "Jujutsu Kaisen Episode 1.mp4",
                    "Jujutsu Kaisen Episode 2.mp4",
                    "Jujutsu Kaisen Episode 3.mp4"
                ]
            }
        }

        self.manga_database = {
            "one piece": {
                "chapters": ["Chapter 1", "Chapter 2", "Chapter 3", "Chapter 4"],
                "image_folder": r"D:\oop 2 project\OnePiece"
            },
            "demon slayer": {
                "chapters": ["Chapter 1", "Chapter 2", "Chapter 3"],
                "image_folder": r"D:\oop 2 project\DemonSlayer"
            },
            "jujutsu kaisen": {
                "chapters": ["Chapter 1", "Chapter 2", "Chapter 3"],
                "image_folder": r"D:\oop 2 project\JujutsuKaisen"
            }
        }
        self.users_data = "users.xlsx"
        self.ratings_data = "ratings.xlsx"
        self.create_user_data_file()
        self.create_ratings_data_file()
        self.logged_in = False

    def create_user_data_file(self):
        if not os.path.exists(self.users_data):
            df = pd.DataFrame(columns=['username', 'password'])
            df.to_excel(self.users_data, index=False)

    def create_ratings_data_file(self):
        if not os.path.exists(self.ratings_data):
            df = pd.DataFrame(columns=['title', 'type', 'rating'])
            df.to_excel(self.ratings_data, index=False)

    def sign_up(self):
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        if not self.user_exists(username):
            new_data = {'username': [username], 'password': [password]}
            df = pd.DataFrame(new_data)
            existing_df = pd.read_excel(self.users_data)
            df = pd.concat([existing_df, df], ignore_index=True)
            df.to_excel(self.users_data, index=False)
            print("Sign up successful!")
        else:
            print("Username already exists. Please choose a different username.")

    def user_exists(self, username):
        df = pd.read_excel(self.users_data)
        return username in df['username'].values

    def login(self):
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        df = pd.read_excel(self.users_data)
        if ((df['username'] == username) & (df['password'] == password)).any():
            print("Login successful!")
            self.logged_in = True
            return True
        else:
            print("Invalid username or password.")
            return False

    def rate_media(self):
        print("Select media type to rate:")
        print("1. Anime")
        print("2. Manga")
        choice = input("Enter your choice (1/2): ")
        if choice == "1":
            self.rate_anime()
        elif choice == "2":
            self.rate_manga()
        else:
            print("Invalid choice")

    def rate_anime(self):
        print("Available Anime to rate:")
        for anime_title in self.anime_database:
            print(f"- {anime_title.capitalize()}")
        anime_title = input("Enter anime title to rate: ").lower()
        if anime_title in self.anime_database:
            rating = self.get_rating()
            self.save_rating(anime_title, 'anime', rating)
        else:
            print("Anime not found.")

    def rate_manga(self):
        print("Available Manga to rate:")
        for manga_title in self.manga_database:
            print(f"- {manga_title.capitalize()}")
        manga_title = input("Enter manga title to rate: ").lower()
        if manga_title in self.manga_database:
            rating = self.get_rating()
            self.save_rating(manga_title, 'manga', rating)
        else:
            print("Manga not found.")

    def get_rating(self):
        while True:
            try:
                rating = float(input("Enter rating (0-10): "))
                if 0 <= rating <= 10:
                    return rating
                else:
                    print("Rating must be between 0 and 10.")
            except ValueError:
                print("Please enter a valid number.")

    def save_rating(self, title, media_type, rating):
        new_rating = {'title': [title], 'type': [media_type], 'rating': [rating]}
        df = pd.DataFrame(new_rating)
        existing_df = pd.read_excel(self.ratings_data)
        df = pd.concat([existing_df, df], ignore_index=True)
        df.to_excel(self.ratings_data, index=False)
        print("Rating saved!")

    def view_ratings(self):
        df = pd.read_excel(self.ratings_data)
        if df.empty:
            print("No ratings available.")
        else:
            print("Ratings:")
            print(df)

    def select_media(self):
        if not self.logged_in:
            if not self.login():
                return
        print("Select an option:")
        print("1. Anime")
        print("2. Manga")
        print("3. Ratings")
        choice = input("Enter your choice (1/2/3): ")
        if choice == "1":
            anime = Anime(self.anime_database)
            anime.select_media()
        elif choice == "2":
            manga = Manga(self.manga_database)
            manga.select_media()
        elif choice == "3":
            self.select_ratings_option()
        else:
            print("Invalid choice")

    def select_ratings_option(self):
        print("Choose an option:")
        print("1. Add Rating")
        print("2. View Ratings")
        choice = input("Enter your choice (1/2): ")
        if choice == "1":
            self.rate_media()
        elif choice == "2":
            self.view_ratings()
        else:
            print("Invalid choice")


# Example usage
mugiwara_tv = MugiwaraTV()
while True:
    print("1. Sign Up")
    print("2. Login")
    print("3. Exit")
    choice = input("Enter your choice: ")
    if choice == "1":
        mugiwara_tv.sign_up()
    elif choice == "2":
        mugiwara_tv.select_media()
    elif choice == "3":
        break
    else:
        print("Invalid choice")                