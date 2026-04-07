<template>
  <div class="min-h-screen bg-gray-50 py-16 px-4">
    <div class="max-w-3xl mx-auto">
      <h1 class="text-3xl font-bold text-gray-900 mb-8">Mentions légales</h1>

      <div class="prose prose-gray max-w-none space-y-8">
        <section v-for="section in sections" :key="section.title" class="card">
          <h2 class="text-xl font-bold text-gray-900 mb-4">{{ section.title }}</h2>
          <div class="text-gray-600 text-sm leading-relaxed space-y-2">
            <p v-for="line in section.content" :key="line">{{ line }}</p>
          </div>
        </section>
      </div>
    </div>
<script setup>
import { useHead } from '@unhead/vue'

useHead({
  title: 'Mentions légales | Zsdevweb',
  meta: [
    { name: 'robots', content: 'noindex, nofollow' }
  ]
})

const sections = [
  {
    title: 'Éditeur du site',
    content: [
      'Zsdevweb — Développeur web freelance',
      'Statut : Auto-entrepreneur',
      'Email : contact@zsdevweb.fr',
      'SIRET : 10297888900016',
    ],
  },
  {
    title: 'Hébergement',
    content: [
      'Ce site est hébergé sur un serveur VPS.',
      'Toutes les données sont stockées en Union Européenne.',
    ],
  },
  {
    title: 'Propriété intellectuelle',
    content: [
      'L\'ensemble du contenu de ce site (textes, images, code) est protégé par le droit d\'auteur.',
      'Toute reproduction sans autorisation écrite est interdite.',
    ],
  },
  {
    title: 'Données personnelles (RGPD)',
    content: [
      'Les données collectées via les formulaires sont utilisées uniquement pour répondre à vos demandes.',
      'Elles ne sont jamais vendues ni cédées à des tiers.',
      'Conformément au RGPD, vous disposez d\'un droit d\'accès, de rectification et de suppression.',
      'Pour exercer ces droits : contact@zsdevweb.fr',
    ],
  },
  {
    title: 'Cookies',
    content: [
      'Ce site utilise des cookies techniques nécessaires à son fonctionnement.',
      'Aucun cookie publicitaire ou de tracking tiers n\'est utilisé.',
    ],
  },
]
</script>
