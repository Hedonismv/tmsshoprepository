from django.urls import path

from .views import (
    BaseSpecView,
    CreateNewFeature,
    CreateNewCategory,
    CreateNewFeatureValidator,
    FeatureChoiceView,
    CreateFeatureView,
    NewProductFeatureView,
    SearchProductAjaxView,
    AttachNewFeatureToProduct,
    ProductFeatureChoicesAjaxView,
    CreateNewProductFeatureAjaxView,
    UpdateProductFeaturesView,
    ShowProductFeaturesForUpdate,
    UpdateProductFeaturesAjaxView
)

urlpatterns = [
    path('', BaseSpecView.as_view(), name='product-list-for-features'),
    path('new-feature/', CreateNewFeature.as_view(), name='new-feature'),
    path('new-category/', CreateNewCategory.as_view(), name='new-category'),
    path('new-validator/', CreateNewFeatureValidator.as_view(), name='new-validator'),
    path('feature-choice/', FeatureChoiceView.as_view(), name='feature-choice-validators'),
    path('feature-create/', CreateFeatureView.as_view(), name='create-feature'),
    path('new-product-feature/', NewProductFeatureView.as_view(), name='new-product-feature'),
    path('search-product/', SearchProductAjaxView.as_view(), name='search-product'),
    path('attach-feature/', AttachNewFeatureToProduct.as_view(), name='attach-feature'),
    path('product-feature/', ProductFeatureChoicesAjaxView.as_view(), name='product-feature'),
    path('attach-new-product-feature/', CreateNewProductFeatureAjaxView.as_view(), name='attach-new-product-feature'),
    path('update-product-features/', UpdateProductFeaturesView.as_view(), name='update-product-features'),
    path('show-product-features-for-update/', ShowProductFeaturesForUpdate.as_view(), name='show-product-features-for-update'),
    path('update-product-features-ajax/', UpdateProductFeaturesAjaxView.as_view(), name='update-product-features-ajax')
]
