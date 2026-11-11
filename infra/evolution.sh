#!/usr/bin/env bash
# 24AGÁ · instala o servidor do WhatsApp (Evolution API) num VPS Ubuntu limpo.
# Uso (no terminal do VPS, como root):
#   curl -fsSL https://24aga.com.br/infra/evolution.sh | bash -s -- wa.24aga.com.br
# Antes: na Hostinger (DNS de 24aga.com.br), crie um registro A  "wa"  apontando para o IP deste VPS.
set -euo pipefail

DOMAIN="${1:-wa.24aga.com.br}"
DIR=/opt/24aga-wa
IMAGE="evoapicloud/evolution-api:v2.3.7"

if [ "$(id -u)" != "0" ]; then echo "Rode como root (sudo -i)."; exit 1; fi
echo "==> 24AGÁ · instalando servidor do WhatsApp em $DOMAIN"

export DEBIAN_FRONTEND=noninteractive
apt-get update -y
apt-get install -y ca-certificates curl ufw openssl dnsutils
if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | sh
fi
systemctl enable --now docker

# firewall: só SSH e web
ufw allow 22/tcp >/dev/null; ufw allow 80/tcp >/dev/null; ufw allow 443/tcp >/dev/null
ufw --force enable >/dev/null

mkdir -p "$DIR"; cd "$DIR"
if [ ! -f .env ]; then
  API_KEY=$(openssl rand -hex 24)
  PG_PASS=$(openssl rand -hex 16)
  cat > .env <<EOF
SERVER_URL=https://$DOMAIN
AUTHENTICATION_API_KEY=$API_KEY
AUTHENTICATION_EXPOSE_IN_FETCH_INSTANCES=false
LANGUAGE=pt-BR
DEL_INSTANCE=false
QRCODE_LIMIT=30
CONFIG_SESSION_PHONE_CLIENT=24AGA
CONFIG_SESSION_PHONE_NAME=Chrome
DATABASE_ENABLED=true
DATABASE_PROVIDER=postgresql
DATABASE_CONNECTION_URI=postgresql://evo:$PG_PASS@postgres:5432/evolution?schema=public
DATABASE_CONNECTION_CLIENT_NAME=evolution_24aga
DATABASE_SAVE_DATA_INSTANCE=true
DATABASE_SAVE_DATA_NEW_MESSAGE=false
DATABASE_SAVE_MESSAGE_UPDATE=false
DATABASE_SAVE_DATA_CONTACTS=false
DATABASE_SAVE_DATA_CHATS=false
CACHE_REDIS_ENABLED=true
CACHE_REDIS_URI=redis://redis:6379/6
CACHE_REDIS_PREFIX_KEY=evolution
CACHE_REDIS_SAVE_INSTANCES=false
CACHE_LOCAL_ENABLED=false
WEBHOOK_GLOBAL_ENABLED=false
LOG_LEVEL=ERROR,WARN
POSTGRES_PASSWORD=$PG_PASS
EOF
  chmod 600 .env
fi
set -a; . ./.env; set +a

cat > docker-compose.yml <<EOF
services:
  evolution:
    image: $IMAGE
    restart: always
    env_file: .env
    volumes: [ "evolution_instances:/evolution/instances" ]
    depends_on: [ postgres, redis ]
  postgres:
    image: postgres:16-alpine
    restart: always
    environment:
      POSTGRES_USER: evo
      POSTGRES_PASSWORD: \${POSTGRES_PASSWORD}
      POSTGRES_DB: evolution
    volumes: [ "pgdata:/var/lib/postgresql/data" ]
  redis:
    image: redis:7-alpine
    restart: always
    command: redis-server --appendonly yes
    volumes: [ "redisdata:/data" ]
  caddy:
    image: caddy:2-alpine
    restart: always
    ports: [ "80:80", "443:443" ]
    volumes: [ "./Caddyfile:/etc/caddy/Caddyfile:ro", "caddy_data:/data", "caddy_config:/config" ]
    depends_on: [ evolution ]
volumes: { evolution_instances: {}, pgdata: {}, redisdata: {}, caddy_data: {}, caddy_config: {} }
EOF

cat > Caddyfile <<EOF
$DOMAIN {
  encode gzip
  reverse_proxy evolution:8080
}
EOF

# atualização automática de segurança do Ubuntu
apt-get install -y unattended-upgrades >/dev/null 2>&1 || true

docker compose pull
docker compose up -d

echo "==> aguardando o servidor subir..."
for i in $(seq 1 60); do
  if curl -fsS "https://$DOMAIN" >/dev/null 2>&1; then break; fi
  sleep 5
done

IP=$(curl -fsS https://api.ipify.org || echo "?")
DNS=$(dig +short "$DOMAIN" | tail -1 || true)
echo
echo "=============================================================="
echo " 24AGÁ · servidor do WhatsApp instalado"
echo " Endereço: https://$DOMAIN"
if [ "$DNS" != "$IP" ]; then
  echo " ATENÇÃO: o DNS de $DOMAIN aponta para '$DNS', mas este VPS é '$IP'."
  echo " Ajuste o registro A 'wa' na Hostinger e rode este script de novo."
fi
echo
echo " Último passo: copie o bloco abaixo, cole no Supabase (SQL Editor) e clique em Run:"
echo
echo "insert into public.app_config (key, value) values"
echo "  ('evolution_url', 'https://$DOMAIN'),"
echo "  ('evolution_key', '$AUTHENTICATION_API_KEY')"
echo "on conflict (key) do update set value = excluded.value, updated_at = now();"
echo
echo " Guarde este bloco só no Supabase: não mande a chave por chat ou e-mail."
echo "=============================================================="
