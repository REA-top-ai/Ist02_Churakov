"""Описание таблиц базы данных через SQLAlchemy."""
from sqlalchemy import Column, Integer, String, Float, ForeignKey  # типы колонок
from sqlalchemy.orm import declarative_base                        # базовый класс для всех моделей

Base = declarative_base()                                  # создаём базовый класс ORM


class User(Base):                                          # таблица пользователей
    __tablename__ = "users"                                # имя таблицы в базе

    id = Column(Integer, primary_key=True)                 # первичный ключ (автоинкремент)
    google_id = Column(String, unique=True)                # уникальный ID пользователя из Google
    name = Column(String)                                  # имя пользователя
    email = Column(String)                                 # email пользователя


class FavoriteMovie(Base):                                 # таблица "хочу посмотреть" (избранные фильмы)
    __tablename__ = "favorite_movies"                      # имя таблицы

    id = Column(Integer, primary_key=True)                 # первичный ключ
    user_id = Column(Integer, ForeignKey("users.id"))      # ссылка на пользователя (внешний ключ)
    name = Column(String)                                  # название фильма
    year = Column(Integer)                                 # год выхода
    rating = Column(Float)                                 # рейтинг (Кинопоиск)
    description = Column(String)                           # краткое описание
