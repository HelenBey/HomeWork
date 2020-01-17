from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import logout, login
from django.shortcuts import render, redirect

from django.http import HttpResponse
from django.views.generic import View, ListView

from lab_app.models import Film, Review

from django.views.decorators.csrf import csrf_exempt
import json
import math

# TODO: Добавить проверку на superuser для отображения кнопки 'Добавить продукт'


# Список продуктов
class ListFilmView(ListView):

    model = Film
    template_name = 'home.html'
    context_object_name = 'films'
    paginate_by = 3

    def get(self, request, page=1):

        elements_on_page = 9

        elements_in_row = 3

        films = Film.objects.all()
        pages_count = math.ceil(len(films) / elements_on_page)

        start_index = (int(page) - 1)*elements_on_page
        end_index = start_index + elements_on_page
        films = films[start_index:end_index]

        index = 1
        rows = []
        row = []
        for film in films:
            row.append(film)

            if index == elements_in_row:
                rows.append(row)
                row = []
                index = 1
            else:
                index += 1

        if len(row) > 0:
            rows.append(row)

        return render(request, 'home.html',  {"films": rows, "page": page, "pages_count": pages_count})


# Страница добавления продукта
class AddFilmView(View):

    def post(self, request):
        if request.POST:
            name = request.POST['filmName']
            description = request.POST['filmDescription']
            image = request.FILES['filmImage']

            film = Film(name=name, description=description, image=image)
            film.save()
            if film is not None:
                return redirect("/")

        return redirect("/invalidFilm")


# Страница с информацией о продукте и отзывами
class FilmView(View):

    def get(self, request, film_id):

        elements_in_row = 2
        film = Film.objects.get(id=film_id)
        reviews = Review.objects.filter(film_id=film_id)
        reviews_count = len(reviews)

        index = 1
        rows = []
        row = []
        for review in reviews:
            row.append(review)

            if index == elements_in_row:
                rows.append(row)
                row = []
                index = 1
            else:
                index += 1

        if len(row) > 0:
            rows.append(row)

        if len(rows) == 0:
            rows = None

        return render(request, 'film.html',  {"film": film, "reviews": rows, "reviews_count": reviews_count})


# Страница регистрации
class SignUpView(View):

    def post(self, request):
        logout(request)
        if request.POST:
            user = User.objects.create_user(
                username=request.POST['username'],
                password=request.POST['password'],
                email=request.POST['email']
            )

            if user is not None:
                login(request, user)
                return redirect("/")

        return redirect("/invalidUser")


# Страница авторизации
class LoginView(View):

    def post(self, request):
        logout(request)
        if request.POST:
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")

        return redirect("/invalidUser")


# Страница выхода
class LogoutView(View):

    def post(self, request):
        logout(request)
        return redirect("/")


class CreateReview(View):

    def post(self, request, film_id):
        if request.POST:
            film = Film.objects.get(id=film_id)
            review_text = request.POST['textReview']
            user = User.objects.get(id=request.user.id)
            review = Review(description=review_text, user=user, film=film)
            review.save()
            if film is not None:
                return redirect("/film/" + film_id)

        return redirect("/invalidFilm")


class AboutView(View):

    def get(self, request):

        # ..

        return render(request, 'about.html')
