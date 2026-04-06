"""
Utilitaires partagés pour le rendu de badges dans l'admin Django.
DRY — une seule définition au lieu de duplication dans chaque admin.
"""
from django.utils.html import format_html


def render_status_badge(status: str, color_map: dict) -> str:
    """
    Retourne un badge HTML coloré pour un statut donné.

    Args:
        status: la valeur du statut (ex: 'accepted', 'hot')
        color_map: dict {status: (couleur_hex, label)}

    Returns:
        HTML sécurisé avec le badge
    """
    color, label = color_map.get(status, ('#6b7280', status))
    return format_html(
        '<span style="background:{};color:white;padding:3px 10px;'
        'border-radius:12px;font-size:11px;font-weight:600">{}</span>',
        color, label,
    )


def render_boolean_badge(value: bool, true_label='Oui', false_label='Non') -> str:
    """Badge vert/gris pour les booléens."""
    color = '#10b981' if value else '#6b7280'
    label = true_label if value else false_label
    return format_html(
        '<span style="background:{};color:white;padding:2px 8px;'
        'border-radius:10px;font-size:11px">{}</span>',
        color, label,
    )


# Palettes de couleurs partagées
QUOTE_STATUS_COLORS = {
    'draft':    ('#6b7280', 'Brouillon'),
    'sent':     ('#3b82f6', 'Envoyé'),
    'viewed':   ('#8b5cf6', 'Consulté'),
    'accepted': ('#10b981', 'Accepté'),
    'rejected': ('#ef4444', 'Refusé'),
    'expired':  ('#f59e0b', 'Expiré'),
}

EMAIL_STATUS_COLORS = {
    'sent':   ('#10b981', 'Envoyé'),
    'failed': ('#ef4444', 'Échoué'),
}
