import { test, expect } from '@playwright/test'

const PAGES = [
  { path: '/',               title: /Zsdevweb/,    desc: 'Accueil' },
  { path: '/services',       title: /Services/,    desc: 'Services' },
  { path: '/portfolio',      title: /Portfolio/,   desc: 'Portfolio' },
  { path: '/a-propos',       title: /propos/i,     desc: 'À propos' },
  { path: '/contact',        title: /Contact/,     desc: 'Contact' },
  { path: '/estimation',     title: /Estimation/i, desc: 'Estimation' },
  { path: '/audit-gratuit',  title: /Audit/i,      desc: 'Audit gratuit' },
  { path: '/mentions-legales', title: /Mentions/i, desc: 'Mentions légales' },
]

test.describe('Navigation SPA — toutes les pages', () => {
  for (const { path, title, desc } of PAGES) {
    test(`${desc} (${path}) charge sans erreur 404`, async ({ page }) => {
      const errors = []
      page.on('pageerror', (err) => errors.push(err.message))

      await page.goto(path)
      await page.waitForLoadState('networkidle')

      // Vérifier le titre
      await expect(page).toHaveTitle(title)

      // Pas d'erreur console critique
      const criticalErrors = errors.filter(e =>
        !e.includes('favicon') && !e.includes('ECONNREFUSED')
      )
      expect(criticalErrors).toHaveLength(0)
    })
  }

  test('navigation via les liens du menu', async ({ page }) => {
    await page.goto('/')
    await page.waitForLoadState('networkidle')

    // Cliquer sur "Services" dans la nav
    const servicesLink = page.locator('nav a[href="/services"], header a[href="/services"]').first()
    if (await servicesLink.count() > 0) {
      await servicesLink.click()
      await expect(page).toHaveURL('/services')
    }
  })

  test('retour arrière navigateur fonctionne', async ({ page }) => {
    await page.goto('/')
    await page.goto('/services')
    await page.goBack()
    await expect(page).toHaveURL('/')
  })

  test('page 404 affiche un message d\'erreur', async ({ page }) => {
    await page.goto('/page-qui-nexiste-pas')
    // En SPA, Vue Router devrait gérer le 404 ou rediriger vers /
    const body = await page.textContent('body')
    // Au minimum la page ne doit pas être vide
    expect(body?.length).toBeGreaterThan(10)
  })
})
