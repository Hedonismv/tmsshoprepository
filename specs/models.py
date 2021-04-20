from django.db import models


class CategoryFeature(models.Model):
    category = models.ForeignKey("mainapp.Category", verbose_name='Категория', on_delete=models.CASCADE)
    feature_name = models.CharField(verbose_name='Имя ключа для категории', max_length=50)
    feature_filter_name = models.CharField(verbose_name='Имя для фильтра', max_length=50)
    unit = models.CharField(max_length=50, verbose_name='Единица измерения', null=True, blank=True)

    class Meta:
        unique_together = ('category', 'feature_name', 'feature_filter_name')

    def __str__(self):
        return f"{self.category.name} | {self.feature_name}"


class FeatureValidator(models.Model):
    category = models.ForeignKey("mainapp.Category", verbose_name='Категория', on_delete=models.CASCADE)
    feature_key = models.ForeignKey(CategoryFeature, verbose_name='Ключ характеристики', on_delete=models.CASCADE)
    valid_feature_value = models.CharField(max_length=100, verbose_name='Валидное значение')

    def __str__(self):
        return f"Категория {self.category.name} | " \
               f"Характристика {self.feature_key.feature_name} | " \
               f"Валидное значение {self.valid_feature_value}"


class ProductFeatures(models.Model):
    product = models.ForeignKey("mainapp.Product", verbose_name='Товар', on_delete=models.CASCADE)
    feature = models.ForeignKey(CategoryFeature, verbose_name='Характеристика', on_delete=models.CASCADE)
    value = models.CharField(max_length=255, verbose_name='Значение')

    def __str__(self):
        return f"Товар - {self.product.title} | " \
               f"Характеристика - {self.feature.feature_name} | " \
               f"Значение - {self.value}"


class SizeFeature(models.Model):
    size_f = models.ForeignKey("mainapp.Size", verbose_name='Размер', on_delete=models.CASCADE)

    def __str__(self):
        return f'Размер - {self.size_f}'
