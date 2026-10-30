#!/usr/bin/env bash
# Passo 1: backup do estado atual (lista de pacotes, APKs de terceiros e configurações).
source "$(dirname "$0")/lib.sh"
conectar

DEST="$BACKUPS/$(date +%Y%m%d-%H%M%S)-backup"
mkdir -p "$DEST/apks"

sh_adb pm list packages -f | sort > "$DEST/pacotes.txt"
sh_adb pm list packages -d | sort > "$DEST/desativados.txt"
for ns in system secure global; do
  sh_adb settings list "$ns" > "$DEST/settings_$ns.txt"
done

# APKs de apps de terceiros (os de sistema continuam na partição /system e voltam com o restaurar)
for pkg in $(sh_adb pm list packages -3 | sed 's/^package://'); do
  for caminho in $(sh_adb pm path "$pkg" | sed 's/^package://'); do
    mkdir -p "$DEST/apks/$pkg"
    adb pull "$caminho" "$DEST/apks/$pkg/" >/dev/null && echo "  $pkg"
  done
done

ok "Backup salvo em $DEST"
