from datetime import date

from django.db.models import Count
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.versioning import AcceptHeaderVersioning

from .models import Restaurant, Menu
from .serializers import (
    RestaurantSerializer,
    MenuSerializer,
    VotingResultSerializer,
    VoteSerializer,
    MenuDetailSerializer,
    MenuListSerializer,
)


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    versioning_class = AcceptHeaderVersioning


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.prefetch_related("voters", "restaurant").filter(
        date=date.today()
    )
    serializer_class = MenuSerializer
    versioning_class = AcceptHeaderVersioning

    def create(self, request, *args, **kwargs):
        """
        Checking for duplicate menus from restaurants
        If you already have today's menu,
        it prevents you from creating a 2nd menu
        """
        today = date.today()
        restaurant = Restaurant.objects.get(pk=request.data.get("restaurant"))

        existing_menu = Menu.objects.filter(
            restaurant=restaurant,
            date=today
        ).exists()

        if existing_menu:
            raise ValidationError(
                "This restaurant has already created a menu for today."
            )

        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "list":
            return MenuListSerializer

        if self.action == "retrieve":
            return MenuDetailSerializer

        if self.action == "voting_results":
            return VotingResultSerializer

        if self.action == "vote":
            return VoteSerializer

        if self.action == "today_menu":
            return VotingResultSerializer

        return super().get_serializer_class()

    @action(detail=True, methods=["POST"], url_path="vote")
    def vote(self, request, pk=None):
        """
        Vote for a specific menu.
        """
        menu = self.get_object()
        serializer = self.get_serializer(menu, data=request.data)

        if serializer.is_valid():
            user = request.user

            if menu.voters.filter(pk=user.pk).exists():
                return Response(
                    "You have already voted for this menu",
                    status=status.HTTP_400_BAD_REQUEST,
                )

            menu.voters.add(user)
            menu.save()

            return Response(
                "Your vote has been recorded", status=status.HTTP_202_ACCEPTED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["GET"], url_path="voting-results")
    def voting_results(self, request):
        """
        Retrieve the voting results for all menus.
        """
        menus = (
            self.get_queryset()
            .annotate(total_votes=Count("voters"))
            .order_by("-total_votes")
        )

        serializer = self.get_serializer(menus, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="today-menu")
    def today_menu(self, request):
        """
        Retrieve today's menu based on the highest number of votes.
        """
        menu = (
            self.get_queryset()
            .annotate(total_votes=Count("voters"))
            .order_by("-total_votes")
        )
        winners = menu.filter(total_votes=menu.first().total_votes)

        serializer = self.get_serializer(winners, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
