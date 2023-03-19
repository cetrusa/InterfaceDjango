from django import forms
from django.contrib import admin
from .models import User,UserProfile, Database

class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserAdminForm(forms.ModelForm):
    databases = forms.ModelMultipleChoiceField(
        queryset=Database.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    class Meta:
        model = User
        fields = '__all__'

class UserAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('username', 'email', 'nombres', 'apellidos', 'genero', 'codregistro')
    filter_horizontal = ('databases',)
    
class DatabaseAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('name')

admin.site.register(Database)
admin.site.register(User,UserAdmin)