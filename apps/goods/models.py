from datetime import datetime
from ckeditor.fields import RichTextField
from django.db import models


class GoodCategory(models.Model):
    """
    商品分类
    """
    CATEGORY_TYPE = (
        (1, '一级分类'),
        (2, '二级分类'),
        (3, '三级分类')
    )
    name = models.CharField(verbose_name='商品名称', max_length=20, help_text='商品名称')
    code = models.CharField(verbose_name='英文名称', max_length=10)
    desc = models.TextField(verbose_name='商品描述')
    category_type = models.IntegerField(verbose_name='分类类型', choices=CATEGORY_TYPE)
    # 自关联
    parent_category = models.ForeignKey('self', null=True, blank=True, related_name='sub_cat', default='',
                                        verbose_name='父级分类',
                                        on_delete=models.CASCADE)
    is_banner = models.BooleanField(verbose_name='是否横幅', default=False)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '商品分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodCategoryBrand(models.Model):
    """
    商标
    """
    category = models.ForeignKey(to=GoodCategory, verbose_name='商品分类', related_name='banner', default='', null=True,
                                 blank=True,
                                 on_delete=models.CASCADE)
    name = models.CharField(verbose_name='品牌名称', max_length=20)
    desc = models.TextField(verbose_name='品牌描述')
    image = models.ImageField(verbose_name='品牌logo', upload_to='brands/%Y/%m/%d')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '品牌名'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Good(models.Model):
    """
    商品信息
    """
    category = models.ForeignKey(to=GoodCategory, verbose_name='商品分类', on_delete=models.CASCADE)
    good_sn = models.CharField(verbose_name='商品编号', max_length=50)
    name = models.CharField(verbose_name='商品名称', max_length=100)
    cover = models.ImageField(verbose_name='商品封面', upload_to='cover/%Y/%m/%d')
    good_num = models.IntegerField('商品数量', default=0)
    sold_num = models.IntegerField(verbose_name='销售数量', default=0)
    click_num = models.IntegerField(verbose_name='点击数量', default=0)
    fav_num = models.IntegerField(verbose_name='收藏数量', default=0)
    good_desc = models.TextField(verbose_name='商品简介')
    market_price = models.FloatField(verbose_name='市场价格', default=0)
    sold_price = models.FloatField(verbose_name='销售价格', default=0)
    good_detail = RichTextField(verbose_name='商品详情', default='')
    is_fare = models.BooleanField(verbose_name='是否包邮', default=False)
    # 考虑机器学习分析
    is_hot = models.BooleanField(verbose_name='是否热卖', default=False)
    is_new = models.BooleanField(verbose_name='是否新品', default=False)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '商品表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodCarouselImage(models.Model):
    """
    商品轮播图片
    """
    good = models.ForeignKey(to=Good, verbose_name='所属商品', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='商品封面', upload_to='banner/%Y/%m/%d')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '轮播图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.good.name


class CarouselGood(models.Model):
    """
    轮播商品
    """
    good = models.ForeignKey(to=Good, verbose_name='所属商品', on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='轮播图', upload_to='banner/%Y/%m/%d')
    index = models.IntegerField(default=1, verbose_name='轮播顺序')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '轮播商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.good.name


class IndexAD(models.Model):
    """
    目录广告位置
    """
    category = models.ForeignKey(to=GoodCategory, related_name='category', verbose_name='商品分类',
                                 on_delete=models.CASCADE)
    good = models.ForeignKey(to=Good, related_name='good', verbose_name='所属商品', on_delete=models.CASCADE)

    class Meta:
        verbose_name = '广告配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.good.name
