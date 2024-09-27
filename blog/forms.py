from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(), required=True)
class FileFieldForm(forms.Form):
    file_field = forms.FileField(widget=forms.ClearableFileInput(), required=True)