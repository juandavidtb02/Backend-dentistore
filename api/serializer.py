from rest_framework import serializers
from .models import Users,Categories,Products,Images_products

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['userid','usermail','username','password_user','userphone','userrole']
        extra_kwargs = {
            'passsword_user':{'write_only':True}
        }


    def create(self,validated_data):
        password = validated_data.pop('password_user',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class CategoriesSerializer(serializers.ModelSerializer):
        class Meta:
            model = Categories
            fields = ['category_id','category_name','category_image']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images_products
        fields = ('image_id', 'image_name', 'image_text')

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('category_id', 'category_name', 'category_image')

class ProductsSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Products
        fields = ('product_id', 'product_name', 'product_price', 'product_stock', 'product_image', 'product_descrip', 'product_details', 'category', 'images')







# class ProductsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Products
#         fields = ['product_id','product_name','product_price','product_stock','product_image','product_descrip','category_id']

class ClientesSerializer(serializers.ModelSerializer):
     date_joined = serializers.DateTimeField(format="%d-%m-%Y")
     class Meta:
          model = Users
          fields = ['userid','usermail','username','userphone','date_joined']

    