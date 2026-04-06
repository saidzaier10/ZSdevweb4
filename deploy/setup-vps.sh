#!/bin/bash
# ============================================================
# Script d'installation initiale du VPS pour Zsdevweb
# Ubuntu 22.04 LTS recommandé
#
# Usage (en root ou avec sudo) :
#   bash setup-vps.sh
# ============================================================
set -e

DOMAIN="${DOMAIN:-zsdevweb.fr}"
ACME_EMAIL="${ACME_EMAIL:-contact@zsdevweb.fr}"
APP_USER="deploy"
APP_DIR="/opt/zsdevweb"

echo "============================================"
echo " Zsdevweb VPS Setup"
echo " Domaine : $DOMAIN"
echo "============================================"

# ---- 1. Mises à jour système ----
echo "→ Mise à jour du système..."
apt-get update -qq
apt-get upgrade -y -qq

# ---- 2. Dépendances ----
echo "→ Installation des dépendances..."
apt-get install -y -qq \
    curl wget git vim htop \
    ufw fail2ban \
    ca-certificates gnupg lsb-release

# ---- 3. Docker ----
echo "→ Installation de Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
fi

# ---- 4. Docker Compose ----
echo "→ Installation de Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
        -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# ---- 5. Utilisateur de déploiement ----
echo "→ Création de l'utilisateur $APP_USER..."
if ! id "$APP_USER" &>/dev/null; then
    useradd -m -s /bin/bash "$APP_USER"
    usermod -aG docker "$APP_USER"
fi

# ---- 6. Répertoire de l'application ----
echo "→ Création du répertoire $APP_DIR..."
mkdir -p "$APP_DIR"
chown "$APP_USER:$APP_USER" "$APP_DIR"

# ---- 7. Firewall UFW ----
echo "→ Configuration du firewall..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# ---- 8. Fail2ban ----
echo "→ Configuration de fail2ban..."
systemctl enable fail2ban
systemctl start fail2ban

# ---- 9. Réseau Docker pour Traefik ----
echo "→ Création du réseau Docker traefik-public..."
docker network create traefik-public 2>/dev/null || echo "  → Réseau déjà existant"

# ---- 10. Résumé ----
echo ""
echo "============================================"
echo " Installation terminée !"
echo "============================================"
echo ""
echo "Prochaines étapes :"
echo "  1. Copier les fichiers de déploiement :"
echo "     scp deploy/* $APP_USER@$DOMAIN:$APP_DIR/"
echo ""
echo "  2. Créer le fichier .env :"
echo "     cp $APP_DIR/.env.example $APP_DIR/.env && nano $APP_DIR/.env"
echo ""
echo "  3. Générer le hash pour le dashboard Traefik :"
echo "     docker run --rm httpd:2.4-alpine htpasswd -nb admin MON_MOT_DE_PASSE"
echo "     → Ajouter dans .env : TRAEFIK_DASHBOARD_AUTH=admin:\$\$hash"
echo ""
echo "  4. Déployer Traefik :"
echo "     cd $APP_DIR"
echo "     docker-compose -f docker-compose.traefik.yml up -d"
echo ""
echo "  5. Déployer l'application :"
echo "     docker-compose -f docker-compose.vps.yml up -d"
echo ""
echo "  6. Créer le superutilisateur Django :"
echo "     docker-compose -f docker-compose.vps.yml exec backend python manage.py createsuperuser"
