from datetime import timedelta

from django.db.models import Count, Q, Value, IntegerField, F
from django.utils import timezone

from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from stories.serializers import StorySerializer
from stories.models import Story, SeenStory


class StoryViewSet(ListModelMixin, RetrieveModelMixin, GenericViewSet):
    serializer_class = StorySerializer
    pagination_class = None  # убираем пагинацию, так как stories не должны делится по страницам
    
    def get_queryset(self):
        today = timezone.now()
        yesterday = today - timedelta(days=1)

        # Проверка пользователь аутентифицирован или нет
        if self.request.user.is_authenticated:
            # если пользователь аутентифицирован, то считаем количество просмотренных
            seen_count = Count('users_seen__id', distinct=True,
                               filter=Q(users_seen__user=self.request.user))
        else:
            # если пользователь не аутентифицирован, то количество просмотренных 0
            seen_count = Value(0, output_field=IntegerField())
        return Story.objects.filter(
            created_at__date__gte=yesterday.date()
        ).annotate(
            title=F(f'title_{self.request.LANGUAGE_CODE}'),
            seen_count=seen_count  # аннотация количества просмотренных
        ).order_by(
            'seen_count'  # сортировка по возрастанию количество просмотров текущим пользователем; если уже просмотрел то последний в списке
        )

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Проверка пользователь аутентифицирован или нет
        if self.request.user.is_authenticated:
            # если пользователь аутентифицирован, то добавляем стори в просмотренные
            SeenStory.objects.get_or_create(user=self.request.user, story=instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
