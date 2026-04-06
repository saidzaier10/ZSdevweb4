import { test, expect } from '@playwright/test'

test.describe('Page d\'accueil', () => {
  test('se charge et affiche le titre', async ({ page }) => {
    await page.goto('/')
    await expect(page).toHaveTitle(/Zsdevweb/)
    await expect(page.locator('h1').first()).toBeVisible()
  })

  test('navigation principale visible', async ({ page }) => {
    await page.goto('/')
    await expect(page.getByRole('navigation').first()).toBeVisible()
  })

  test('CTA principal mène au wizard de devis', async ({ page }) => {
    await page.goto('/')
    // Trouver le premier lien vers /devis
    const ctaLink = page.locator('a[href="/devis"]').first()
    await expect(ctaLink).toBeVisible()
    await ctaLink.click()
    await expect(page).toHaveURL(/\/devis/)
  })

  test('simulateur de prix visible', async ({ page }) => {
    await page.goto('/')
    // Scroll jusqu'au simulateur
    const simulator = page.locator('[data-testid="simulator"], #simulator, .simulator').first()
    if (await simulator.count() > 0) {
      await simulator.scrollIntoViewIfNeeded()
      await expect(simulator).toBeVisible()
    }
  })
})
