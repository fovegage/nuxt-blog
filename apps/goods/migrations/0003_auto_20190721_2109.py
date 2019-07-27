# Generated by Django 2.1 on 2019-07-21 13:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_goodcategorybrand_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='goodcarouselimage',
            name='image',
            field=models.ImageField(upload_to='banner/', verbose_name='商品封面'),
        ),
        migrations.AlterField(
            model_name='goodcategory',
            name='code',
            field=models.CharField(max_length=10, verbose_name='英文名称'),
        ),
        migrations.AlterField(
            model_name='goodcategory',
            name='parent_category',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_cat', to='goods.GoodCategory', verbose_name='父级分类'),
        ),
        migrations.AlterField(
            model_name='goodcategorybrand',
            name='image',
            field=models.ImageField(upload_to='brands/', verbose_name='品牌logo'),
        ),
    ]