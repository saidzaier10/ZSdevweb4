"""
RecommendationService — Recommandations intelligentes selon le type de projet.
"""


class RecommendationService:

    # Map: slug du type de projet → slugs des options recommandées prioritaires
    RECOMMENDATIONS = {
        'vitrine-simple': ['seo', 'analytics', 'maintenance'],
        'vitrine-premium': ['seo', 'blog-cms', 'analytics', 'multilingue', 'maintenance'],
        'boutique-ecommerce': ['paiement-en-ligne', 'seo', 'analytics', 'email-automation', 'maintenance'],
        'marketplace': ['paiement-en-ligne', 'analytics', 'email-automation', 'chatbot-ia', 'maintenance'],
        'webapp-metier': ['analytics', 'maintenance', 'email-automation'],
        'saas-plateforme': ['analytics', 'email-automation', 'chatbot-ia', 'multilingue', 'maintenance'],
    }

    # Messages de recommandation contextuels
    MESSAGES = {
        'seo': {
            'title': 'Référencement SEO',
            'reason': 'Un site vitrine sans SEO reste invisible sur Google. Le SEO vous apporte du trafic organique gratuit sur le long terme.',
            'roi': 'En moyenne, le SEO génère 5× plus de leads que les autres canaux.',
        },
        'paiement-en-ligne': {
            'title': 'Paiement en ligne',
            'reason': 'Indispensable pour votre boutique. Stripe, PayPal et Apple Pay couvrent 95% des préférences de paiement.',
            'roi': 'Un checkout optimisé peut augmenter votre taux de conversion de 30%.',
        },
        'analytics': {
            'title': 'Analytics avancé',
            'reason': 'Sans données, vous naviguez à l\'aveugle. Comprendre votre trafic, c\'est optimiser vos conversions.',
            'roi': 'Les entreprises data-driven convertissent 6× mieux.',
        },
        'email-automation': {
            'title': 'Automatisation emails',
            'reason': 'Relancez automatiquement vos prospects, fidélisez vos clients sans effort manuel.',
            'roi': 'L\'email marketing génère en moyenne 42€ pour 1€ investi.',
        },
        'maintenance': {
            'title': 'Maintenance mensuelle',
            'reason': 'Mises à jour de sécurité, sauvegardes quotidiennes et monitoring 24/7. Votre site toujours en ligne.',
            'roi': 'Coût d\'une panne non maintenue : 4× plus cher que la maintenance préventive.',
        },
        'blog-cms': {
            'title': 'Blog / CMS',
            'reason': 'Le content marketing génère 3× plus de leads que la publicité traditionnelle, pour un coût 62% inférieur.',
            'roi': 'Les entreprises qui bloguent ont 55% plus de visiteurs.',
        },
        'multilingue': {
            'title': 'Site multilingue',
            'reason': 'Ouvrez votre activité aux marchés internationaux. 72% des internautes achètent dans leur langue.',
            'roi': 'Un site multilingue peut multiplier votre marché adressable par 3 à 5.',
        },
        'chatbot-ia': {
            'title': 'Chatbot IA',
            'reason': 'Qualifiez vos leads 24h/24 et répondez instantanément aux questions de vos visiteurs.',
            'roi': 'Les chatbots réduisent les coûts de support de 30% et augmentent les conversions de 15%.',
        },
    }

    @classmethod
    def get_recommendations_for_quote(cls, quote) -> list:
        """
        Retourne une liste de recommandations contextuelles pour un devis.
        Exclut les options déjà sélectionnées.
        """
        if not quote.project_type:
            return []

        project_slug = quote.project_type.slug
        selected_slugs = set(quote.options.values_list('slug', flat=True))

        recommended_slugs = cls.RECOMMENDATIONS.get(project_slug, [])

        from services_catalog.models import SupplementaryOption
        recommendations = []

        for slug in recommended_slugs:
            if slug in selected_slugs:
                continue

            try:
                option = SupplementaryOption.objects.get(slug=slug, is_active=True)
                message = cls.MESSAGES.get(slug, {})
                recommendations.append({
                    'option': {
                        'id': option.pk,
                        'name': option.name,
                        'slug': option.slug,
                        'price': str(option.price),
                        'is_recurring': option.is_recurring,
                    },
                    'reason': message.get('reason', ''),
                    'roi': message.get('roi', ''),
                })
            except SupplementaryOption.DoesNotExist:
                continue

        return recommendations[:3]  # Max 3 recommandations

    @classmethod
    def get_generic_recommendations(cls, project_type_slug: str) -> list:
        """
        Recommandations génériques sans devis (pour le wizard en cours).
        """
        from services_catalog.models import SupplementaryOption

        recommended_slugs = cls.RECOMMENDATIONS.get(project_type_slug, [])
        result = []

        for slug in recommended_slugs[:3]:
            try:
                option = SupplementaryOption.objects.get(slug=slug, is_active=True)
                message = cls.MESSAGES.get(slug, {})
                result.append({
                    'id': option.pk,
                    'name': option.name,
                    'slug': option.slug,
                    'price': str(option.price),
                    'is_recurring': option.is_recurring,
                    'reason': message.get('reason', ''),
                    'roi': message.get('roi', ''),
                })
            except SupplementaryOption.DoesNotExist:
                continue

        return result
