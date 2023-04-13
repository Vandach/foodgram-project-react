from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView
from rest_framework import generics

from .forms import AddRecipeForm, LoginUserForm, RegisterUserForm
from .models import Recipe
from .serializers import RecipeSerializer
from rest_framework import viewsets


from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'


class RecipeViewSet(viewsets.ModelViewSet):
    pagination_class = StandardResultsSetPagination
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

# menu = [
#         {'title': "первая", 'url_name': 'first'},
#         {'title': "вторая", 'url_name': 'second'},
#         {'title': "третья", 'url_name': 'third'},
# ]


# class FoodHome(DataMixin, ListView):
#     model = Recipe
#     template_name = 'index.html'
#     context_object_name = 'recipies'

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Главная страница')
#         # context['menu'] = menu
#         # context['title'] = 'Главная'
#         # context['cat_selected'] = 0
#         context = dict(list(context.items()) + list(c_def.items()))
#         return context

#     def get_queryset(self):
#         return Recipe.objects.filter(is_published=True)


# def categoties(request, catid):
#     if (request.POST):
#         print(request.POST)

#     return HttpResponse(f"Страница категорий {catid}")


# def archive(request, year):
#     if int(year) > 2023:
#         return redirect('home', permanent=True)
#     return HttpResponse(f"Страница архива {year}")


# def pageNotFound(request, exception):
#     return HttpResponseNotFound('Страница не найдена')


# class AddPage(LoginRequiredMixin, DataMixin, CreateView):
#     form_class = AddRecipeForm
#     template_name = 'addrecipe.html'
#     success_url = reverse_lazy('home')
#     login_url = reverse_lazy('home')
#     raise_exception = True

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Добавление статьи')
#         context = dict(list(context.items()) + list(c_def.items()))
#         return context


# class ShowRecipe(DataMixin, DetailView):
#     model = Recipe
#     template_name = 'index2.html'
#     slug_url_kwarg = 'recipe_slug'
#     context_object_name = 'recipe'

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title=context['recipe'])
#         context = dict(list(context.items()) + list(c_def.items()))
#         # context['title'] = context['recipe']
#         # context['menu'] = menu
#         return context


# class ShowCategory(DataMixin, ListView):
#     model = Recipe
#     template_name = 'index.html'
#     context_object_name = 'recipies'
#     allow_empty = False

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(
#             title=context['recipies'][0].cat,
#             cat_selected=context['recipies'][0].cat_id
#             )
#         context = dict(list(context.items()) + list(c_def.items()))
#         # context['title'] = 'Категория -' + str(context['recipies'][0].cat)
#         # context['menu'] = menu
#         # context['cat_selected'] = context['recipies'][0].cat_id
#         return context

#     def get_queryset(self):
#         return Recipe.objects.filter(
#             cat__slug=self.kwargs['cat_slug'], is_published=True
#             )


# class RegisterUser(DataMixin, CreateView):
#     form_class = RegisterUserForm
#     template_name = 'register.html'
#     success_url = reverse_lazy('home')

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Регистрация')
#         context = dict(list(context.items()) + list(c_def.items()))
#         return context

#     def form_valid(self, form):
#         user = form.save()
#         login(self.request, user)
#         return redirect('home')


# class LoginUser(DataMixin, LoginView):
#     form_class = LoginUserForm
#     template_name = 'login.html'

#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         c_def = self.get_user_context(title='Авторизация')
#         context = dict(list(context.items()) + list(c_def.items()))
#         return context

#     def get_success_url(self) -> str:
#         return reverse_lazy('home')


# def logout_user(request):
#     logout(request)
#     return redirect('login')


# class RecipeAPIView(generics.ListAPIView):
#     queryset = Recipe2.objects.all()
#     serializer_class = RecipeSerializer
