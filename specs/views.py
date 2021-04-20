from collections import defaultdict

from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect, JsonResponse

from .models import CategoryFeature, FeatureValidator, ProductFeatures
from .forms import NewCategoryFeatureKeyForm, NewCategoryForm
from mainapp.models import Category, Product


class BaseSpecView(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'product_features.html', {})


class CreateNewFeature(View):

    def get(self, request, *args, **kwargs):
        form = NewCategoryFeatureKeyForm(request.POST or None)
        context = {'form': form}
        return render(request, 'new_feature.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCategoryFeatureKeyForm(request.POST or None)
        if form.is_valid():
            new_category_feature_key = form.save(commit=False)
            new_category_feature_key.category = form.cleaned_data['category']
            new_category_feature_key.feature_name = form.cleaned_data['feature_name']
            new_category_feature_key.save()
        return HttpResponseRedirect('/product-specs/')


class CreateNewCategory(View):

    def get(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        context = {'form': form}
        return render(request, 'new_category.html', context)

    def post(self, request, *args, **kwargs):
        form = NewCategoryForm(request.POST or None)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.name = form.cleaned_data['name']
            new_category.save()
        return HttpResponseRedirect('/product-specs/')


class CreateNewFeatureValidator(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'new_validator.html', context)


class FeatureChoiceView(View):

    def get(self, request, *args, **kwargs):
        option = '<option value="{value}">{option_name}</option>'
        html_select = """
            <select class="form-select" name="feature-validators" id="feature-validators-id" aria-label="Default select example">
                <option selected>---</option>
                {result}
            </select>
                    """
        feature_key_qs = CategoryFeature.objects.filter(
            category_id=int(request.GET.get('category_id'))
        )
        res_string = ""
        for item in feature_key_qs:
            res_string += option.format(value=item.feature_name, option_name=item.feature_name)
        html_select = html_select.format(result=res_string)
        return JsonResponse({"result": html_select, "value": int(request.GET.get('category_id'))})


class CreateFeatureView(View):

    def get(self, request, *args, **kwargs):
        category_id = request.GET.get('category_id')
        feature_name = request.GET.get('feature_name')
        value = request.GET.get('feature_value').strip(" ")
        print(value)
        category = Category.objects.get(id=int(category_id))
        feature = CategoryFeature.objects.get(category=category, feature_name=feature_name)
        existed_object, created = FeatureValidator.objects.get_or_create(
            category=category,
            feature_key=feature,
            valid_feature_value=value
        )
        if not created:
            return JsonResponse({
                "error": f"Значение '{value}' уже существует."
            })
        messages.add_message(
            request, messages.SUCCESS,
            f'Значение "{value}" для характеристики '
            f'"{feature.feature_name}" в категории {category.name} успешно создано'
        )
        return JsonResponse({'result': 'ok'})


class NewProductFeatureView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'new_product_feature.html', context)


class SearchProductAjaxView(View):

    def get(self, request, *args, **kwargs):
        query = request.GET.get('query')
        category_id = request.GET.get('category_id')
        category = Category.objects.get(id=int(category_id))
        products = list(Product.objects.filter(
            category=category,
            title__icontains=query
        ).values())
        return JsonResponse({"result": products})


class AttachNewFeatureToProduct(View):

    def get(self, request, *args, **kwargs):
        res_string = ""
        product = Product.objects.get(id=int(request.GET.get('product_id')))
        existing_features = list(set([item.feature.feature_name for item in product.features.all()]))
        print(existing_features)
        category_features = CategoryFeature.objects.filter(
            category=product.category
        ).exclude(feature_name__in=existing_features)
        option = '<option value="{value}">{option_name}</option>'
        html_select = """
            <select class="form-select" name="product-category-features" id="product-category-features-id" aria-label="Default select example">
                <option selected>---</option>
                {result}
            </select>
                    """
        for item in category_features:
            res_string += option.format(value=item.category.id, option_name=item.feature_name)
        html_select = html_select.format(result=res_string)
        return JsonResponse({"features": html_select})


class ProductFeatureChoicesAjaxView(View):

    def get(self, request, *args, **kwargs):
        res_string = ""
        category = Category.objects.get(id=int(request.GET.get('category_id')))
        feature_key = CategoryFeature.objects.get(
            category=category,
            feature_name=request.GET.get('product_feature_name')
        )
        validators_qs = FeatureValidator.objects.filter(
            category=category,
            feature_key=feature_key
        )
        option = '<option value="{value}">{option_name}</option>'
        html_select = """
            <select class="form-select" name="product-category-features-choices" id="product-category-features-choices-id" aria-label="Default select example">
                <option selected>---</option>
                {result}
            </select>
                    """
        for item in validators_qs:
            res_string += option.format(value=item.id, option_name=item.valid_feature_value)
        html_select = html_select.format(result=res_string)
        return JsonResponse({"features": html_select})


class CreateNewProductFeatureAjaxView(View):

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(title=request.GET.get('product'))
        category_feature = CategoryFeature.objects.get(
            category=product.category,
            feature_name=request.GET.get('category_feature')
        )
        value = request.GET.get('value')
        feature = ProductFeatures.objects.create(
            feature=category_feature,
            product=product,
            value=value
        )
        product.features.add(feature)
        return JsonResponse({"OK": "OK"})


class UpdateProductFeaturesView(View):

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        context = {'categories': categories}
        return render(request, 'update_product_features.html', context)


class ShowProductFeaturesForUpdate(View):

    def get(self, request, *args, **kwargs):
        product = Product.objects.get(id=int(request.GET.get('product_id')))
        features_values_qs = product.features.all()
        head = """
        <hr>
            <div class="row">
                <div class="col-md-4">
                    <h4 class="text-center">Характеристика</h4>
                </div>
                <div class="col-md-4">
                    <h4 class="text-center">Текущее значение</h4>
                </div>
                <div class="col-md-4">
                    <h4 class="text-center">Новое значение</h4>
                </div>
            </div>
        <div class='row'>{}</div>
        <div class="row">
        <hr>
        <div class="col-md-4">
        </div>
        <div class="col-md-4">
            <p class='text-center'><button class="btn btn-success" id="save-updated-features">Сохранить</button></p> 
        </div>
        <div class="col-md-4">
        </div>
        </div>
        """
        option = '<option value="{value}">{option_name}</option>'
        select_values = """
            <select class="form-select" name="feature-value" id="feature-value" aria-label="Default select example">
                <option selected>---</option>
                {result}
            </select>
                    """
        mid_res = ""
        select_different_values_dict = defaultdict(list)
        for item in features_values_qs:
            fv_qs = FeatureValidator.objects.filter(
                category=item.product.category,
                feature_key=item.feature
            ).values()
            for fv in fv_qs:
                if fv['valid_feature_value'] == item.value:
                    pass
                else:
                    select_different_values_dict[fv['feature_key_id']].append(fv['valid_feature_value'])
            feature_field = '<input type="text" class="form-control" id="{id}" value="{value}" disabled/>'
            current_feature_value = """
            <div class='col-md-4 feature-current-value' style='margin-top:10px; margin-bottom:10px;'>{}</div>
                                    """
            body_feature_field = """
            <div class='col-md-4 feature-name' style='margin-top:10px; margin-bottom:10px;'>{}</div>
                                """
            body_feature_field_value = """
            <div class='col-md-4 feature-new-value' style='margin-top:10px; margin-bottom:10px;'>{}</div>
            """
            body_feature_field = body_feature_field.format(feature_field.format(id=item.feature.id, value=item.feature.feature_name))
            current_feature_value_mid_res = ""
            for item_ in select_different_values_dict[item.feature.id]:
                current_feature_value_mid_res += option.format(value=item.feature.id, option_name=item_)
            body_feature_field_value = body_feature_field_value.format(
                select_values.format(item.feature.id, result=current_feature_value_mid_res)
            )
            current_feature_value = current_feature_value.format(feature_field.format(id=item.feature.id, value=item.value))
            m = body_feature_field + current_feature_value + body_feature_field_value
            mid_res += m
        result = head.format(mid_res)
        return JsonResponse({"result": result})


class UpdateProductFeaturesAjaxView(View):

    def post(self, request, *args, **kwargs):
        features_names = request.POST.getlist('features_names')
        features_current_values = request.POST.getlist('features_current_values')
        new_feature_values = request.POST.getlist('new_feature_values')
        data_for_update = [{'feature_name': name, 'current_value': curr_val, 'new_value': new_val} for name, curr_val, new_val
                           in zip(features_names, features_current_values, new_feature_values)]
        product = Product.objects.get(title=request.POST.get('product'))
        for item in product.features.all():
            for item_for_update in data_for_update:
                if item.feature.feature_name == item_for_update['feature_name']:
                    if item.value != item_for_update['new_value'] and item_for_update['new_value'] != '---':
                        cf = CategoryFeature.objects.get(
                            category=product.category,
                            feature_name=item_for_update['feature_name']
                        )
                        item.value = FeatureValidator.objects.get(
                            category=product.category,
                            feature_key=cf,
                            valid_feature_value=item_for_update['new_value']
                        ).valid_feature_value
                        item.save()
        messages.add_message(
            request, messages.SUCCESS,
            f'Значения характеристик для товара {product.title} успешно обновлены'
        )
        return JsonResponse({"result": "ok"})
