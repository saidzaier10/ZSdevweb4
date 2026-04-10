"""
Sitemap dynamique Django — inclus les pages statiques et les projets portfolio.
Référencé dans robots.txt → https://zsdevweb.fr/sitemap.xml
"""
from django.contrib.sitemaps import Sitemap
from portfolio.models import PortfolioProject


class StaticPagesSitemap(Sitemap):
    """Pages statiques du frontend SPA."""
    priority = 0.8
    changefreq = 'weekly'
    protocol = 'https'

    def items(self):
        return [
            {'loc': '/', 'priority': 1.0, 'changefreq': 'daily'},
            {'loc': '/services', 'priority': 0.9},
            {'loc': '/portfolio', 'priority': 0.8},
            {'loc': '/a-propos', 'priority': 0.6},
            {'loc': '/contact', 'priority': 0.7},
            {'loc': '/estimation', 'priority': 0.8},
            {'loc': '/devis', 'priority': 0.7},
            {'loc': '/audit-gratuit', 'priority': 0.7},
        ]

    def location(self, item):
        return item['loc']

    def priority(self, item):
        return item.get('priority', 0.5)

    def changefreq(self, item):
        return item.get('changefreq', 'weekly')


class PortfolioSitemap(Sitemap):
    """Pages portfolio individuelles (dynamiques, basées sur la BDD)."""
    changefreq = 'monthly'
    priority = 0.7
    protocol = 'https'

    def items(self):
        return PortfolioProject.objects.filter(is_published=True)

    def location(self, obj):
        return f'/portfolio/{obj.slug}'

    def lastmod(self, obj):
        return obj.created_at


# Dictionnaire exporté pour urls.py
sitemaps = {
    'static': StaticPagesSitemap,
    'portfolio': PortfolioSitemap,
}
