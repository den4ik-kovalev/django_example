from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import ModelSerializer, Serializer, IntegerField
from rest_framework.views import APIView

from events.dispatcher import EventsDispatcher
from events.models import User, Event


class GetUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class GetEventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"

    participants = GetUserSerializer(many=True)


class CreateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "password", "first_name", "last_name", "birthdate")
        extra_kwargs = {"birthdate": {"required": False}}


class CreateEventSerializer(ModelSerializer):
    class Meta:
        model = Event
        fields = ("header", "text")


class ChangeParticipantSerializer(Serializer):
    event_id = IntegerField()


class DeleteEventSerializer(Serializer):
    event_id = IntegerField()


class CreateUserView(APIView):
    """ Регистрация пользователя """

    def post(self, request: Request) -> Response:
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = EventsDispatcher.create_user(
                username=serializer.validated_data["username"],
                password=serializer.validated_data["password"],
                first_name=serializer.validated_data["first_name"],
                last_name=serializer.validated_data["last_name"],
                birthdate=serializer.validated_data.get("birthdate"),
            )
        except EventsDispatcher.Error as e:
            return Response({"error": str(e)})
        else:
            return Response({
                "error": None,
                "result": GetUserSerializer(user).data
             })


class CreateEventView(APIView):
    """ Создание события """

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        serializer = CreateEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        current_user = EventsDispatcher.get_current_user(request.user)

        event = EventsDispatcher.create_event(
            header=serializer.validated_data["header"],
            text=serializer.validated_data["text"],
            creator=current_user,
        )

        return Response({
            "error": None,
            "result": GetEventSerializer(event).data
        })


class GetEventListView(APIView):
    """ Получение списка событий """

    permission_classes = (IsAuthenticated,)

    def get(self, request: Request) -> Response:
        user_id = request.GET.get("user_id")
        if user_id:
            user_id = int(user_id)

        event_list = EventsDispatcher.get_events(user_id)

        return Response({
            "error": None,
            "result": GetEventSerializer(event_list, many=True).data
        })


class AddParticipantView(APIView):
    """ Участие в событии """

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        serializer = ChangeParticipantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event_id = serializer.validated_data["event_id"]

        if not EventsDispatcher.is_event_exist(event_id):
            return Response({"error": "Event is not exist"})

        event = Event.objects.get(id=event_id)
        current_user = EventsDispatcher.get_current_user(request.user)

        try:
            EventsDispatcher.add_participant(event, current_user)
        except EventsDispatcher.Error as e:
            return Response({"error": str(e)})
        else:
            return Response({
                "error": None,
                "result": GetEventSerializer(event).data
             })


class RemoveParticipantView(APIView):
    """ Отмена участия в событии """

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        serializer = ChangeParticipantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event_id = serializer.validated_data["event_id"]

        if not EventsDispatcher.is_event_exist(event_id):
            return Response({"error": "События не существует"})

        event = Event.objects.get(id=event_id)
        current_user = EventsDispatcher.get_current_user(request.user)

        try:
            EventsDispatcher.remove_participant(event, current_user)
        except EventsDispatcher.Error as e:
            return Response({"error": str(e)})
        else:
            return Response({
                "error": None,
                "result": GetEventSerializer(event).data
            })


class DeleteEventView(APIView):
    """ Удаление события создателем """

    permission_classes = (IsAuthenticated,)

    def post(self, request: Request) -> Response:
        serializer = DeleteEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event_id = serializer.validated_data["event_id"]

        if not EventsDispatcher.is_event_exist(event_id):
            return Response({"error": "События не существует"})

        event = Event.objects.get(id=event_id)
        current_user = EventsDispatcher.get_current_user(request.user)

        try:
            EventsDispatcher.delete_event(event, current_user)
        except EventsDispatcher.Error as e:
            return Response({"error": str(e)})
        else:
            return Response({"error": None})
