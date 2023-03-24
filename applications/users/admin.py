from django import forms
from django.contrib import admin
from .models import User,UserProfile, Database,RegistroAuditoria

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
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Filtra los permisos para incluir permisos personalizados y permisos predeterminados
        form.base_fields['user_permissions'].queryset = form.base_fields['user_permissions'].queryset.filter(
            content_type__app_label__in=['applications.home', 'auth', 'contenttypes', 'sessions', 'admin']
        )
        # Cambia el widget de user_permissions y groups a CheckboxSelectMultiple
        # form.base_fields['user_permissions'].widget = forms.CheckboxSelectMultiple()
        # form.base_fields['groups'].widget = forms.CheckboxSelectMultiple()
        return form

    
class DatabaseAdmin(admin.ModelAdmin):
    form = UserAdminForm
    list_display = ('name')

admin.site.register(RegistroAuditoria)
admin.site.register(Database)
admin.site.register(User,UserAdmin)




