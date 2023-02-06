
from django.urls import path
from .views import RegisterView,LoginView,UserView,LogoutView,CategoriesView,ProductsView,ClientsView,ImagesProductsView,CategoriesNameView,ColorsView,ProductColorView
urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('categories/', CategoriesView.as_view()),
    path('categories-names/', CategoriesNameView.as_view()),
    path('products/',ProductsView.as_view()),
    path('clientes/',ClientsView.as_view()),
    path('imagesProducts/',ImagesProductsView.as_view()),
    path('colors/',ColorsView.as_view()),
    path('productcolors/',ProductColorView.as_view()),


]
