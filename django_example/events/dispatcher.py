from datetime import datetime
from typing import Optional

from django.db import transaction
from django.contrib.auth.models import User as DjangoUser

from .models import User, Event


class EventsDispatcher:
    """ Логика работы модуля Событий """

    class Error(Exception):
        pass

    @classmethod
    def is_username_taken(cls, username: str) -> bool:
        """ Есть ли пользователь с таким логином """
        return User.objects.filter(username=username).exists()

    @classmethod
    def create_user(
        cls,
        username: str,
        password: str,
        first_name: str,
        last_name: str,
        birthdate: Optional[datetime] = None
    ):
        """ Регистрация нового пользователя """

        # проверка не занят ли логин
        if cls.is_username_taken(username):
            raise cls.Error("Имя пользователя уже занято")

        try:
            # в рамках одной транзакции
            with transaction.atomic():

                # создание пользователя Django
                DjangoUser.objects.create_user(
                    username=username,
                    email="",
                    password=password
                )

                # создание пользователя в отдельной таблице
                user = User.objects.create(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    birthdate=birthdate
                )
        except Exception:
            raise

        return user

    @classmethod
    def get_current_user(
        cls,
        django_user: DjangoUser
    ):
        """ Текущий пользователь из таблицы User """
        return User.objects.get(username=django_user.username)

    @classmethod
    def get_events(cls, user_id: Optional[int] = None):
        """ Список событий с поиском по участнику """
        if user_id:
            return Event.objects.filter(participants__id=user_id)
        return Event.objects.all()

    @classmethod
    def is_event_exist(cls, event_id: int) -> bool:
        """ Существует ли событие с данным ID """
        return Event.objects.filter(id=event_id).exists()

    @classmethod
    def create_event(
        cls,
        header: str,
        text: str,
        creator: User,
    ):
        """ Создание нового события """

        # создание события в таблице
        event = Event.objects.create(
            header=header,
            text=text,
            creator=creator
        )

        return event

    @classmethod
    def add_participant(
        cls,
        event: Event,
        user: User
    ) -> None:
        """ Добавить участника в событие """

        if user in event.participants.all():
            raise cls.Error("Пользователь уже является участником события")

        event.participants.add(user)
        event.save()

    @classmethod
    def remove_participant(
        cls,
        event: Event,
        user: User
    ) -> None:
        """ Убрать участника из события """

        if user not in event.participants.all():
            raise cls.Error("Пользователь не является участником события")

        event.participants.remove(user)
        event.save()

    @classmethod
    def delete_event(
        cls,
        event: Event,
        delete_user: User
    ) -> None:
        """ Удалить событие """

        if delete_user != event.creator:
            raise cls.Error("Пользователь не является создателем события")

        event.delete()
