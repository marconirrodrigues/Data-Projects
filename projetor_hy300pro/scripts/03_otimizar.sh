#!/usr/bin/env bash
# Passo 3: ajustes de desempenho/interface que não mexem no hardware do projetor.
#   DNS_PRIVADO=dns.adguard-dns.com ./scripts/03_otimizar.sh 192.168.0.50
source "$(dirname "$0")/lib.sh"
conectar

# Animações mais curtas deixam a navegação no controle mais rápida (1.0 = padrão)
ESCALA="${ESCALA_ANIMACAO:-0.5}"
sh_adb settings put global window_animation_scale     "$ESCALA"
sh_adb settings put global transition_animation_scale "$ESCALA"
sh_adb settings put global animator_duration_scale    "$ESCALA"
ok "Animações em ${ESCALA}x"

# DNS privado (Android 9+) bloqueia anúncios/telemetria na rede sem precisar de root
if [[ -n "${DNS_PRIVADO:-}" ]]; then
  sh_adb settings put global private_dns_mode hostname
  sh_adb settings put global private_dns_specifier "$DNS_PRIVADO"
  ok "DNS privado: $DNS_PRIVADO"
fi

# Launcher padrão: LAUNCHER=com.spocky.projengmenu (Projectivy). Faça isto ANTES do debloat.
if [[ -n "${LAUNCHER:-}" ]]; then
  atividade="$(sh_adb cmd package resolve-activity --brief -a android.intent.action.MAIN \
    -c android.intent.category.HOME "$LAUNCHER" | tail -1)"
  sh_adb cmd package set-home-activity "$atividade" && ok "Launcher padrão: $atividade"
fi

# Libera cache e recompila apps em segundo plano para abrir mais rápido
sh_adb pm trim-caches 999G >/dev/null 2>&1 || true
sh_adb cmd package bg-dexopt-job >/dev/null 2>&1 || true
ok "Cache limpo e otimização de apps disparada"
