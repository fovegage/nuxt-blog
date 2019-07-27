from django.contrib import admin
from .models import Good, GoodCategory, GoodCarouselImage, GoodCategoryBrand, CarouselGood, IndexAD

admin.site.register(GoodCategoryBrand)
admin.site.register(GoodCategory)
admin.site.register(Good)
admin.site.register(GoodCarouselImage)
admin.site.register(CarouselGood)
admin.site.register(IndexAD)