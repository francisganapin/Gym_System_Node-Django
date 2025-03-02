from django import forms
from .models import gym_members,gym_trainor,gym_classes
from django.core.exceptions import ValidationError



class RegisterFormMember(forms.ModelForm):
    expiry = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d'],
        label="Expiry Date"
    )
    def clean_phone_number(self):
            data = self.cleaned_data['phone_number']
            if not data.isdigit():
                raise ValidationError(_('Invalid phone number - digits only'))

            return data

    class Meta:
        model = gym_members
        fields = ['id_card', 'expiry', 'membership', 'first_name', 'last_name', 'phone_number', 'address']


class RegisterFormClass(forms.ModelForm):
     
    class Meta:
        model = gym_classes
        fields = ['class_name','class_type','class_day','class_hour','trainor_name']
     


class RegisterFormTrainor(forms.ModelForm):
    class Meta:
         model = gym_trainor
         fields = ['trainor_id','first_name','last_name','specialty','phone_number']