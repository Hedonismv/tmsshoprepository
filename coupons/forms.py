from django import forms

from coupons.models import Coupon


class CouponApplyForm(forms.Form):
    code = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].label = 'Введите промокод'

    def clean_code(self):
        promo_code = self.cleaned_data['code']
        if Coupon.objects.filter(code=promo_code).exists():
            return promo_code
        else:
            raise forms.ValidationError(
                f'Такого промокода нет'
            )

    class Meta:
        model = Coupon
        fields = ['code']
