from django import forms
from .models import Lead

class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'phone', 'description', 'file']
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 5 * 1024 * 1024:  # 5 MB
                raise forms.ValidationError("Размер файла не должен превышать 5 МБ.")
            if not file.name.endswith('.pdf'):
                raise forms.ValidationError("Разрешены только файлы формата PDF.")
        return file
