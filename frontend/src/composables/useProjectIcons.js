const UPDATE_ICONS = {
  progress: {
    template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-blue-600"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" /></svg>`,
  },
  milestone: {
    template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-green-600"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 3l14 9-14 9V3z" /></svg>`,
  },
  delivery: {
    template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-purple-600"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" /></svg>`,
  },
  feedback: {
    template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-amber-600"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" /></svg>`,
  },
  info: {
    template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-gray-500"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>`,
  },
  default: {
    template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-gray-400"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" /></svg>`,
  },
}

const DOC_ICONS = {
  contract:    { template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-blue-600"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>` },
  mockup:      { template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-purple-600"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>` },
  deliverable: { template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-green-600"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" /></svg>` },
  invoice:     { template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-amber-600"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 14l6-6m-5.5.5h.01m4.99 5h.01M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16l3.5-2 3.5 2 3.5-2 3.5 2zM10 8.5a.5.5 0 11-1 0 .5.5 0 011 0zm5 5a.5.5 0 11-1 0 .5.5 0 011 0z" /></svg>` },
  other:       { template: `<svg fill="none" viewBox="0 0 24 24" stroke="currentColor" class="text-gray-500"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" /></svg>` },
}

const UPDATE_ICON_BG = {
  progress:  'bg-blue-50',
  milestone: 'bg-green-50',
  delivery:  'bg-purple-50',
  feedback:  'bg-amber-50',
  info:      'bg-gray-50',
}

const DOC_COLORS = {
  contract:    'bg-blue-50',
  mockup:      'bg-purple-50',
  deliverable: 'bg-green-50',
  invoice:     'bg-amber-50',
  other:       'bg-gray-50',
}

const DOC_LABELS = {
  contract: 'Contrat', mockup: 'Maquette', deliverable: 'Livrable', invoice: 'Facture', other: 'Document',
}

export function useProjectIcons() {
  return {
    updateIconSvg:   (type) => UPDATE_ICONS[type]  ?? UPDATE_ICONS.default,
    updateIconClass: (type) => UPDATE_ICON_BG[type] ?? 'bg-gray-50',
    docIconSvg:      (type) => DOC_ICONS[type]     ?? DOC_ICONS.other,
    docColor:        (type) => DOC_COLORS[type]     ?? 'bg-gray-50',
    docTypeLabel:    (type) => DOC_LABELS[type]     ?? 'Document',
  }
}
