from django.contrib import admin
from .models import ZoneIrrigation

@admin.register(ZoneIrrigation)
class ZoneIrrigationAdmin(admin.ModelAdmin):
    list_display = ('nom_zone', 'superficie', 'type_sol', 'besoin_eau', 'user')  # Colonnes affichées dans la vue liste
    list_filter = ('type_sol', 'user')  # Filtres par type de sol ou utilisateur
    search_fields = ('nom_zone', 'type_sol')  # Champs de recherche par nom ou type de sol
    ordering = ('nom_zone',)  # Trie les zones par nom par défaut
    list_per_page = 0  # Affiche toutes les zones sur une seule page

    fieldsets = (
        (None, {
            'fields': ('nom_zone', 'superficie', 'type_sol', 'besoin_eau', 'user', 'image_zone')
        }),
    )
