
from django.urls import path
from .views import RegisterView,LoginView,UserView,LogoutView,CategoriesView,ProductsView,ClientsView,ImagesProductsView
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('categories/', CategoriesView.as_view()),
    path('products/',ProductsView.as_view()),
    path('clientes/',ClientsView.as_view()),
    path('imagesProducts/',ImagesProductsView.as_view()),


]
