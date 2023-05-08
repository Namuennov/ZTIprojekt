from django.contrib.auth import authenticate, get_user_model, login as auth_login, logout as auth_logout
from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Author, Opus, Category, Review, Comment
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .forms import ReviewForm, CommentForm

def index(request):
    authorsList = Author.objects.all().order_by('name')
    categoriesList = Category.objects.all().order_by('name')
    context = {
        'authorsList': authorsList,
        'categoriesList': categoriesList,
    }
    return render(request, 'tCap_reviews/index.html', context)

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            group = Group.objects.get(name='Normies')
            group.user_set.add(user)
            messages.success(request, ("Zarejestrowano pomyślnie, teraz możesz się zalogować"))
            return redirect('tCap_reviews:index')
    else:
        form = UserCreationForm()

    return render(request, 'tCap_reviews/register.html', {
        'form': form,
    })

def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('tCap_reviews:index')
            else:
                return redirect('tCap_reviews:login')
    else:
        form = AuthenticationForm()

    return render(request, 'tCap_reviews/login.html', {
        'form': form,
    })

def logout(request):
    auth_logout(request)
    messages.success(request, ("Wylogowano pomyślnie!"))
    return redirect('tCap_reviews:index')

def searchAuthor(request):
    if request.method == "POST":
        searchedPhrase = request.POST['searchedPhrase']
        results = Author.objects.filter(name__contains=searchedPhrase)
        return render(request, 'tCap_reviews/searchAuthor.html', {
            'results': results,
        })
    else:
        return redirect('tCap_reviews:index')

def searchOpus(request):
    if request.method == "POST":
        searchedPhrase = request.POST['searchedPhrase']
        results = Opus.objects.filter(name__contains=searchedPhrase)
        return render(request, 'tCap_reviews/searchOpus.html', {
            'results': results,
        })
    else:
        return redirect('tCap_reviews:index')

def authorPage(request, authorId):
    author = get_object_or_404(Author, id=authorId)
    #authorOpuses = get_list_or_404(Opus, authorId=author.id)
    authorOpuses = Opus.objects.filter(authorId=author.id)
    context = {
        'author': author,
        'authorOpuses': authorOpuses
    }
    return render(request, 'tCap_reviews/authorPage.html', context)

def categoryPage(request, categoryId):
    category = get_object_or_404(Category, id=categoryId)
    categoryOpuses = get_list_or_404(Opus, categoryId=category.id)
    context = {
        'category': category,
        'categoryOpuses': categoryOpuses
    }
    return render(request, 'tCap_reviews/categoryPage.html', context)

def opusPage(request, opusId):
    opus = get_object_or_404(Opus, id=opusId)
    opusReviews = Review.objects.filter(opusId=opusId)
    reviewsList = []
    for review in opusReviews:
        reviewer = get_object_or_404(get_user_model(), id=review.userId_id)
        reviewsList.append((review.id, reviewer.username, review.rating))
    didUserSubmittedReview = False
    userReview = None
    if request.user.is_authenticated and request.user.is_staff:
        try:
            userReview = Review.objects.get(opusId=opusId, userId=request.user.id)
        except:
            userReview = None
        if userReview is not None:
            didUserSubmittedReview = True
    context = {
        'opus': opus,
        'didUserSubmittedReview': didUserSubmittedReview,
        'userReview': userReview,
        'reviewsList': reviewsList,
    }
    return render(request, 'tCap_reviews/opusPage.html', context)

def reviewPage(request, opusId, reviewId, wasCommentSubmitted=False):
    opus = get_object_or_404(Opus, id=opusId)
    review = get_object_or_404(Review, id=reviewId)
    reviewer = get_object_or_404(get_user_model(), id=review.userId_id)
    reviewComments = Comment.objects.filter(reviewId=review.id)
    commentsList = []
    for comment in reviewComments:
        user = get_object_or_404(get_user_model(), id=comment.userId_id)
        commentsList.append((comment.id, user.username, comment.content))

    if request.method == "POST" and not wasCommentSubmitted:
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            comment = commentForm.save(commit=False)
            comment.reviewId = review
            comment.userId = request.user
            comment.save()
            wasCommentSubmitted = True
            return reviewPage(request, opusId, reviewId, wasCommentSubmitted)
    else:
        commentForm = CommentForm

    context = {
        'opus': opus,
        'review': review,
        'reviewer': reviewer,
        'commentsList': commentsList,
        'commentForm': commentForm,
    }
    return render(request, 'tCap_reviews/reviewPage.html', context)

def addReview(request, opusId):

    if not request.user.is_staff or not request.user.is_authenticated:
        return redirect('tCap_reviews:index')

    opus = get_object_or_404(Opus, id=opusId)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.opusId = opus
            review.userId = request.user
            review.save()
            return opusPage(request, opusId)
    else:
        form = ReviewForm

    return render(request, 'tCap_reviews/addReview.html', {
        'form': form,
        'opus': opus,
    })

def editReview(request, opusId, reviewId):

    if not request.user.is_staff or not request.user.is_authenticated:
        return redirect('tCap_reviews:index')

    review = Review.objects.get(id=reviewId)
    opus = get_object_or_404(Opus, id=opusId)

    form = ReviewForm(request.POST or None, instance=review)
    if form.is_valid():
        review = form.save(commit=False)
        review.opusId = opus
        review.userId = request.user
        review.save()
        return opusPage(request, opusId)

    return render(request, 'tCap_reviews/editReview.html', {
        'form': form,
        'opus': opus,
        'review': review,
    })
