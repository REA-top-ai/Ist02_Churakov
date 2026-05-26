"""Подключение к базе данных SQLite."""
from sqlalchemy import create_engine                       # создание движка БД
from sqlalchemy.orm import sessionmaker                    # фабрика сессий

from db.models import Base                                 # базовый класс моделей

engine = create_engine("sqlite:///movies.db")             # создаём движок: файл movies.db в текущей папке
Session = sessionmaker(bind=engine)                        # фабрика для создания сессий БД


def init_db():                                             # функция инициализации БД
    """Создаёт все таблицы при первом запуске."""
    Base.metadata.create_all(engine)                       # создаём таблицы из моделей (если их ещё нет)
