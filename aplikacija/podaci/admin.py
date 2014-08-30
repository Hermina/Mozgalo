from django.contrib import admin
from podaci.models import Beer, Review, UpdateBeer

class ReviewAdmin(admin.ModelAdmin):
    list_filter = ['created']

admin.site.register(Beer)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UpdateBeer)

# TODO edit admin site (view)
