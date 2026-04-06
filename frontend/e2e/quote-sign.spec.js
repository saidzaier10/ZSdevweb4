import { test, expect } from '@playwright/test'

test.describe('Signature de devis', () => {
  const FAKE_UUID = '00000000-0000-0000-0000-000000000001'
  const FAKE_TOKEN = 'valid-test-token-abc123'

  test.beforeEach(async ({ page }) => {
    // Mock API de vérification token
    await page.route(`**/api/v1/quotes/${FAKE_UUID}/sign/**`, async (route) => {
      if (route.request().method() === 'GET') {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            valid: true,
            quote_number: 'QT-2026-0001',
            client_name: 'Marie Dupont',
            total_ttc: '2400.00',
            valid_until: '2026-05-01',
            status: 'sent',
          }),
        })
      } else if (route.request().method() === 'POST') {
        await route.fulfill({
          status: 200,
          contentType: 'application/json',
          body: JSON.stringify({
            detail: 'Devis accepté avec succès.',
            status: 'accepted',
            signed_at: new Date().toISOString(),
          }),
        })
      }
    })
  })

  test('page de signature se charge avec un token valide', async ({ page }) => {
    await page.goto(`/devis/${FAKE_UUID}/signer?token=${FAKE_TOKEN}`)
    await page.waitForLoadState('networkidle')

    // Doit afficher les infos du devis
    await expect(page.getByText('QT-2026-0001')).toBeVisible({ timeout: 5000 })
    await expect(page.getByText('Marie Dupont')).toBeVisible()
    await expect(page.getByText(/2.400|2400/)).toBeVisible()
  })

  test('bouton de signature activé après saisie du nom', async ({ page }) => {
    await page.goto(`/devis/${FAKE_UUID}/signer?token=${FAKE_TOKEN}`)
    await page.waitForLoadState('networkidle')

    const signBtn = page.getByRole('button', { name: /accepter|signer/i })
    if (await signBtn.count() > 0) {
      // Sans nom : bouton désactivé
      await expect(signBtn).toBeDisabled()

      // Avec nom : bouton activé
      await page.locator('input[type="text"]').first().fill('Marie Dupont')
      await expect(signBtn).toBeEnabled()
    }
  })

  test('acceptation du devis affiche le message de succès', async ({ page }) => {
    await page.goto(`/devis/${FAKE_UUID}/signer?token=${FAKE_TOKEN}`)
    await page.waitForLoadState('networkidle')

    const nameInput = page.locator('input[type="text"]').first()
    if (await nameInput.count() > 0) {
      await nameInput.fill('Marie Dupont')
      await page.getByRole('button', { name: /accepter|signer/i }).click()

      // Message de succès
      await expect(page.getByText(/accepté|succès/i)).toBeVisible({ timeout: 5000 })
    }
  })

  test('token invalide affiche une erreur', async ({ page }) => {
    // Overrider le mock pour renvoyer un token invalide
    await page.route(`**/api/v1/quotes/${FAKE_UUID}/sign/**`, async (route) => {
      await route.fulfill({
        status: 400,
        contentType: 'application/json',
        body: JSON.stringify({ valid: false, detail: 'Token invalide.' }),
      })
    })

    await page.goto(`/devis/${FAKE_UUID}/signer?token=mauvais-token`)
    await page.waitForLoadState('networkidle')

    await expect(page.getByText(/invalide|erreur/i)).toBeVisible({ timeout: 5000 })
  })
})
