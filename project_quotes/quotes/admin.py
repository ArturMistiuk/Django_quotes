from django.contrib import admin
from .models import Quote, Tag, Author

# Register your models here.
admin.site.register(Quote)
admin.site.register(Author)
admin.site.register(Tag)
