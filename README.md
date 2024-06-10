Если модель должна поддерживать Импорт экспорт, то нужно admin.py наследоваться от ImportExportModelAdmin 
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin

class BlogAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    ...


Transition
python3 manage.py update_translation_fields - синхронизировать данные
python3 manage.py makemessages -l ru
django-admin compilemessages - применить языковый перевод