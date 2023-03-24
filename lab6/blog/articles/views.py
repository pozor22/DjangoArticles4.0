from .models import Article
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout

def get_article(request, article_id):
    try:
        post = Article.objects.get(id=article_id)
        return render(request, 'article.html', {"post": post})
    except Article.DoesNotExist:
        raise Http404

def archive(request):
    return render(request, 'archive.html',{"posts": Article.objects.all()})

def exit(request):
    logout(request)
    return render(request, 'archive.html',{"posts": Article.objects.all()})

def authorization(request):
    if request.method == "POST":
        form = {
            'password': request.POST["password"], 'login': request.POST["login"]
        }
        if form["password"] and form["login"]:
            user = authenticate(username=form["login"], password=form["password"])
            if user == None:
                form['errors'] = u"Данного пользователя не существует"
                return render(request, 'authorization.html', {'form': form})
            else:
                login(request, user)
                return redirect('/article/', article_id=Article.id)
        else:
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'authorization.html', {'form': form})
    else:
        return render(request, "authorization.html")

def create_user(request):
    if request.method == "POST":
        form = {
            'password': request.POST["password"], 'login': request.POST["login"], 'mail': request.POST["mail"]
        }
        if form["password"] and form["login"] and form["mail"]:
            try:
                User.objects.get(username=form["login"])
                form['errors'] = u"Данный пользователь уже существует"
                return render(request, 'create_user.html', {'form': form})
            except:
                User.objects.create_user(form["login"], form["mail"], form["password"])
                return redirect('/article/', article_id=Article.id)
        else:
            form['errors'] = u"Не все поля заполнены"
            return render(request, 'create_user.html', {'form': form})
    else:
        return render(request, 'create_user.html')

def create_post(request):
    if not request.user.is_anonymous:
        if request.method == "POST":
            # обработать данные формы, если метод POST
            form = {
                'text': request.POST["text"], 'title': request.POST["title"]
            }
            # в словаре form будет храниться информация, введенная пользователем
            if form["text"] and form["title"]:
                # если поля заполнены без ошибок
                flag = 0
                for i in Article.objects.all():
                    if form["title"] == i.title:
                        flag = 1
                        break
                if flag == 0:
                    Article.objects.create(text=form["text"], title=form["title"], author=request.user)
                    return redirect('/article/', article_id=Article.id)
                else:
                    form['errors'] = u"Имя вашей статьи не уникальное"
                    return render(request, 'create_post.html', {'form': form})
            # перейти на страницу поста
            else:
                # если введенные данные некорректны
                form['errors'] = u"Не все поля заполнены"
                return render(request, 'create_post.html', {'form': form})
        else:
            # просто вернуть страницу с формой, если метод GET
            return render(request, 'create_post.html', {})

    else:
        raise Http404

