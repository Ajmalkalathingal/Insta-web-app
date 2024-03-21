from django import forms
from .models import Comm
from .models import RATING

class ProductReviewForm(forms.ModelForm):
    review = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Write your review',
                'class': 'form-control m-3',
                'rows': '4',  # Adjust the number of rows as needed
            }
        )
    )

    rating = forms.ChoiceField(
        choices=RATING,
        widget=forms.Select(
            attrs={
                'class': 'custom-select m-3 rounded bg-light pt-1',
                'style': 'border: none;',  # Remove border
            }
        )
    )

    class Meta:
        model = ProductReview
        fields = ['review', 'rating']
