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

useHead({
  title: 'Création de site web TPE/PME — Mouvaux & Lille Metropole | Zsdevweb',
  meta: [
    { name: 'description', content: 'Développeur web freelance basé à Mouvaux. J\'accompagne les TPE et PME de la métropole lilloise (Hem, Roubaix, Tourcoing) dans la création de leurs sites et applications sur-mesure.' },
    { property: 'og:title', content: 'Création de site web TPE/PME — Mouvaux & Lille Metropole | Zsdevweb' },
    { property: 'og:description', content: 'Développeur web freelance basé à Mouvaux. Expert dans la digitalisation des TPE et PME Hauts-de-France.' },
    { property: 'og:type', content: 'website' }
  ]
})
</script>
