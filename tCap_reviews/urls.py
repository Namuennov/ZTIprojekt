from django.urls import path

from . import views

app_name = "tCap_reviews"
urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('searchAuthor', views.searchAuthor, name='searchAuthor'),
    path('searchOpus', views.searchOpus, name='searchOpus'),
    path('authors/<int:authorId>', views.authorPage, name='authorPage'),
    path('categories/<int:categoryId>', views.categoryPage, name='categoryPage'),
    path('opuses/<int:opusId>', views.opusPage, name='opusPage'),
    path('opuses/<int:opusId>/<int:reviewId>', views.reviewPage, name='reviewPage'),
    path('opuses/<int:opusId>/addReview', views.addReview, name='addReview'),
    path('opuses/<int:opusId>/<int:reviewId>/editReview', views.editReview, name='editReview'),
]
