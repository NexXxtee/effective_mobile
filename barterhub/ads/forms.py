from django import forms
from .models import Ad, ExchangeProposal

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']
        labels = {
            'title': 'Заголовок',
            'description': 'Описание',
            'image_url': 'URL изображения',
            'category': 'Категория',
            'condition': 'Состояние',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'image_url': forms.URLInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
        }
        

class ExchangeProposalForm(forms.ModelForm):
    ad_sender = forms.ModelChoiceField(
        queryset=Ad.objects.none(), # Передается пустой queryset, будет заполнен в __init__
        label="Ваше объявление для обмена",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    comment = forms.CharField(
        label="Комментарий",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        required=False
    )

    class Meta:
        model = ExchangeProposal
        fields = ['ad_sender', 'comment']

    # Пользователь будет видеть только свои объявления
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['ad_sender'].queryset = Ad.objects.filter(user=user)