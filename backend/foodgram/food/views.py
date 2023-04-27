from typing import Any
from django.shortcuts import get_object_or_404
from requests import Request
from rest_framework.response import Response
from .models import Recipe, User, Tag, Ingredient, RecipeIngredients, ShoppingCart
from .serializers import (RecipeSerializer, RecipeCreateSerializer,
                          TagSerializer, IngredientSerializer,
                          RecipeIngredientsSerializer, RecipeIngredients2Serializer,
                        )
from django.template.loader import render_to_string
from datetime import datetime
from django.db.models import Sum
from rest_framework import viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.http import HttpResponse
from .utils import get_list_ingredients
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'


class RecipeViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Recipe.objects.all()


    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return RecipeSerializer
        return RecipeCreateSerializer


    @action(methods=('get',), detail=False)
    def download_shopping_cart(self, request):
        final_list = {}
        ingredients = RecipeIngredients.objects.filter(
            recipe__shopping__user=request.user).values_list(
            'ingredient__name', 'ingredient__measurement_unit',
            'amount')
        for item in ingredients:
            name = item[0]
            if name not in final_list:
                final_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                final_list[name]['amount'] += item[2]
        pdfmetrics.registerFont(
            TTFont('Impact', 'Impact.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = ('attachment; '
                                           'filename="shopping_list.pdf"')
        page = canvas.Canvas(response)
        page.setFont('Impact', size=24)
        page.drawString(200, 800, 'Список ингредиентов')
        page.setFont('Impact', size=16)
        height = 750
        for i, (name, data) in enumerate(final_list.items(), 1):
            page.drawString(75, height, (f'<{i}> {name} - {data["amount"]}, '
                                         f'{data["measurement_unit"]}'))
            height -= 25
        page.showPage()
        page.save()
        return response




class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class RecipeIngredientsViewSet(viewsets.ModelViewSet):
    queryset = RecipeIngredients.objects.all()
    serializer_class = RecipeIngredientsSerializer



class test(viewsets.ModelViewSet):
    queryset = RecipeIngredients.objects.all()
    serializer_class = RecipeIngredients2Serializer