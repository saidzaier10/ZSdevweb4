<template>
  <div>
    <HeroSection />
    <ServicesSection />
    <ProcessSection />
    <SimulatorSection />
    <PortfolioSection />
    <PricingTiersSection />
    <TestimonialsSection />
    <FaqSection />
    <CtaSection />
  </div>
</template>

<script setup>
import HeroSection from '@/components/home/HeroSection.vue'
import ServicesSection from '@/components/home/ServicesSection.vue'
import ProcessSection from '@/components/home/ProcessSection.vue'
import SimulatorSection from '@/components/home/SimulatorSection.vue'
import PortfolioSection from '@/components/home/PortfolioSection.vue'
import PricingTiersSection from '@/components/home/PricingTiersSection.vue'
import TestimonialsSection from '@/components/home/TestimonialsSection.vue'
import FaqSection from '@/components/home/FaqSection.vue'
import CtaSection from '@/components/home/CtaSection.vue'
import { useHead } from '@unhead/vue'

// Données FAQ pour le JSON-LD FAQPage (Google Rich Snippets)
const faqItems = [
  { q: 'Quel est le délai pour un projet ?', a: 'Un site vitrine est livré en 2 à 4 semaines. Un e-commerce en 4 à 8 semaines. Une application web en 6 à 16 semaines selon la complexité.' },
  { q: 'Comment se déroule le paiement ?', a: '30% à la signature du devis, 40% à mi-projet, 30% à la livraison. Paiement par virement ou carte bancaire.' },
  { q: 'Proposez-vous un suivi après livraison ?', a: 'Oui, une période de garantie de 30 jours est incluse. Des contrats de maintenance mensuelle sont disponibles à partir de 150€/mois.' },
  { q: 'Puis-je modifier le devis après signature ?', a: 'Des modifications mineures sont incluses. Pour des évolutions majeures, un avenant est établi en accord avec vous.' },
  { q: 'Travaillez-vous à distance ?', a: 'Oui, je travaille en 100% remote avec des clients dans toute la France et à l\'international. Des visioconférences régulières assurent le suivi.' },
]

useHead({
  title: 'Création de site web TPE/PME — Mouvaux & Lille Metropole | Zsdevweb',
  meta: [
    { name: 'description', content: 'Développeur web freelance basé à Mouvaux. J\'accompagne les TPE et PME de la métropole lilloise (Hem, Roubaix, Tourcoing) dans la création de leurs sites et applications sur-mesure.' },
    { property: 'og:title', content: 'Création de site web TPE/PME — Mouvaux & Lille Metropole | Zsdevweb' },
    { property: 'og:description', content: 'Développeur web freelance basé à Mouvaux. Expert dans la digitalisation des TPE et PME Hauts-de-France.' },
    { property: 'og:type', content: 'website' },
    { property: 'og:url', content: 'https://zsdevweb.fr/' },
    { name: 'twitter:card', content: 'summary_large_image' },
    { name: 'twitter:title', content: 'Création de site web TPE/PME — Zsdevweb' },
    { name: 'twitter:description', content: 'Développeur web freelance à Mouvaux. Sites et applications sur-mesure pour TPE/PME.' },
  ],
  link: [
    { rel: 'canonical', href: 'https://zsdevweb.fr/' },
  ],
  script: [
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        mainEntity: faqItems.map(item => ({
          '@type': 'Question',
          name: item.q,
          acceptedAnswer: {
            '@type': 'Answer',
            text: item.a,
          },
        })),
      }),
    },
    {
      type: 'application/ld+json',
      innerHTML: JSON.stringify({
        '@context': 'https://schema.org',
        '@type': 'ProfessionalService',
        '@id': 'https://zsdevweb.fr/#business',
        name: 'Zsdevweb',
        url: 'https://zsdevweb.fr',
        telephone: '',
        email: 'contact@zsdevweb.fr',
        description: 'Développeur web freelance spécialisé dans la création de sites et applications sur-mesure pour TPE et PME de la métropole lilloise.',
        founder: {
          '@type': 'Person',
          name: 'Said',
          jobTitle: 'Développeur web freelance',
        },
        address: {
          '@type': 'PostalAddress',
          addressLocality: 'Mouvaux',
          addressRegion: 'Hauts-de-France',
          postalCode: '59420',
          addressCountry: 'FR',
        },
        geo: {
          '@type': 'GeoCoordinates',
          latitude: 50.7008,
          longitude: 3.1167,
        },
        areaServed: [
          { '@type': 'City', name: 'Mouvaux' },
          { '@type': 'City', name: 'Roubaix' },
          { '@type': 'City', name: 'Tourcoing' },
          { '@type': 'City', name: 'Hem' },
          { '@type': 'City', name: 'Lille' },
        ],
        serviceType: ['Création de site web', 'Application web sur-mesure', 'E-commerce', 'SaaS'],
        priceRange: '€€',
        aggregateRating: {
          '@type': 'AggregateRating',
          ratingValue: '5',
          reviewCount: '12',
          bestRating: '5',
          worstRating: '1',
        },
        sameAs: [
          'https://github.com/zsdevweb',
          'https://www.linkedin.com/in/zsdevweb',
        ],
      }),
    },
  ],
})
</script>

