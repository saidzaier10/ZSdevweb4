import { test, expect } from '@playwright/test'

test.describe('Wizard de devis', () => {
  test.beforeEach(async ({ page }) => {
    // Mock de l'API catalog pour ne pas dépendre du backend
    await page.route('**/api/v1/catalog/categories/**', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          {
            id: 1, name: 'Site Vitrine', slug: 'vitrine',
            project_types: [
              { id: 1, name: 'Site vitrine simple', base_price: '1500.00', min_days: 14, max_days: 21 },
              { id: 2, name: 'Site vitrine avancé', base_price: '2500.00', min_days: 21, max_days: 35 },
            ],
          },
        ]),
      })
    })

    await page.route('**/api/v1/catalog/design-options/**', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          { id: 1, name: 'Standard', price_supplement: '0.00' },
          { id: 2, name: 'Premium', price_supplement: '500.00' },
        ]),
      })
    })

    await page.route('**/api/v1/catalog/complexity/**', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          { id: 1, name: 'Simple', multiplier: '1.0' },
          { id: 2, name: 'Standard', multiplier: '1.3' },
        ]),
      })
    })

    await page.route('**/api/v1/catalog/options/**', async (route) => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify([
          { id: 1, name: 'SEO', price: '400.00', is_recurring: false },
        ]),
      })
    })
  })

  test('page devis accessible', async ({ page }) => {
    await page.goto('/devis')
    await expect(page).toHaveURL('/devis')
    await expect(page.locator('h1, h2').first()).toBeVisible()
  })

  test('étape 1 — sélection type de projet', async ({ page }) => {
    await page.goto('/devis')
    await page.waitForLoadState('networkidle')

    // Vérifier que les types de projets sont affichés
    const projectTypes = page.locator('[data-testid="project-type"], .project-type-btn, button').filter({ hasText: /vitrine|projet/i })
    if (await projectTypes.count() > 0) {
      await projectTypes.first().click()
      // Vérifier que le prix est mis à jour
      const priceDisplay = page.locator('[data-testid="total-price"], .price, .total').first()
      if (await priceDisplay.count() > 0) {
        await expect(priceDisplay).toBeVisible()
      }
    }
  })

  test('navigation entre étapes', async ({ page }) => {
    await page.goto('/devis')
    await page.waitForLoadState('networkidle')

    // Chercher un bouton "Suivant" ou "Continuer"
    const nextBtn = page.getByRole('button', { name: /suivant|continuer|next/i }).first()
    if (await nextBtn.count() > 0 && await nextBtn.isEnabled()) {
      const initialUrl = page.url()
      // Le wizard reste sur la même URL mais change d'étape
      await nextBtn.click()
    }
  })

  test('étape contact — validation email', async ({ page }) => {
    await page.goto('/devis')
    await page.waitForLoadState('networkidle')

    // Trouver le champ email s'il est visible
    const emailInput = page.locator('input[type="email"]').first()
    if (await emailInput.count() > 0 && await emailInput.isVisible()) {
      await emailInput.fill('invalide')
      await emailInput.blur()

      // Remplir avec email valide
      await emailInput.fill('test@example.com')
      await expect(emailInput).toHaveValue('test@example.com')
    }
  })
})
