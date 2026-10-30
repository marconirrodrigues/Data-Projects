#!/usr/bin/env bash
# Funções compartilhadas pelos scripts do projeto.
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONFIG="$RAIZ/config"
BACKUPS="$RAIZ/backups"

# Endereço do projetor: ./scripts/xx.sh 192.168.0.50  ou  export HY300_IP=192.168.0.50
HY300_IP="${1:-${HY300_IP:-}}"
ADB_PORTA="${ADB_PORTA:-5555}"

info()  { printf '\033[1;34m[i]\033[0m %s\n' "$*"; }
ok()    { printf '\033[1;32m[ok]\033[0m %s\n' "$*"; }
aviso() { printf '\033[1;33m[!]\033[0m %s\n' "$*"; }
erro()  { printf '\033[1;31m[x]\033[0m %s\n' "$*" >&2; exit 1; }

command -v adb >/dev/null || erro "adb não encontrado. Instale o Android platform-tools."

conectar() {
  if [[ -n "$HY300_IP" ]]; then
    info "Conectando em $HY300_IP:$ADB_PORTA (aceite a autorização na tela do projetor)"
    adb connect "$HY300_IP:$ADB_PORTA" >/dev/null || true
    export ANDROID_SERIAL="$HY300_IP:$ADB_PORTA"
  fi
  adb wait-for-device
  [[ "$(adb get-state 2>/dev/null)" == "device" ]] || erro "Dispositivo não autorizado/offline."
  ok "Conectado: $(adb shell getprop ro.product.model | tr -d '\r')"
}

# </dev/null: sem isso o adb shell consome o stdin dos loops "while read".
sh_adb() { adb shell "$@" </dev/null | tr -d '\r'; }

# Lê um arquivo de lista ignorando comentários (#) e linhas vazias; usa só a 1ª coluna.
ler_lista() { grep -vE '^\s*(#|$)' "$1" | awk '{print $1}'; }

# Como ler_lista, mas mantém a marca opcional ":desativar" da 2ª coluna.
ler_lista_modo() { grep -vE '^\s*(#|$)' "$1" | awk '{print $1, ($2 == ":desativar" ? "desativar" : "")}'; }

instalado() { sh_adb pm list packages | grep -qx "package:$1"; }

# Pacotes de hardware (proteger.txt) e apps desejados (apps.conf) nunca são removidos
protegido() { cat <(ler_lista "$CONFIG/proteger.txt") <(ler_lista "$CONFIG/apps.conf") | grep -qx "$1"; }

# Texto que identifica a placa: plataforma, hardware, flavor e device tree.
id_plataforma() {
  sh_adb 'for p in ro.board.platform ro.hardware ro.build.flavor; do getprop $p; done; tr "\0" " " < /proc/device-tree/compatible 2>/dev/null'
}

# Bloqueia scripts em plataformas não validadas (ver config/plataformas.txt)
checar_plataforma() {
  local ident
  ident="$(id_plataforma | tr '\n' ' ')"
  if ! grep -qiF -f <(ler_lista "$CONFIG/plataformas.txt") <<<"$ident"; then
    aviso "Placa não validada em config/plataformas.txt: $ident"
    [[ "${FORCAR:-0}" == "1" ]] || erro "Abortando. Use FORCAR=1 se tiver certeza."
  fi
  ok "Placa validada: $ident"
}

# Impede qualquer alteração sem um backup deste mesmo aparelho/firmware (feito pelo 01_backup.sh).
exigir_backup() {
  local fp ultimo
  fp="$(sh_adb getprop ro.build.fingerprint)"
  ultimo="$(grep -lxF "$fp" "$BACKUPS"/*-backup/fingerprint.txt 2>/dev/null | sort | tail -1 || true)"
  [[ -n "$ultimo" ]] || erro "Nenhum backup deste aparelho/firmware. Rode antes: ./scripts/01_backup.sh ${HY300_IP}"
  ok "Backup encontrado: $(dirname "$ultimo")"
}
