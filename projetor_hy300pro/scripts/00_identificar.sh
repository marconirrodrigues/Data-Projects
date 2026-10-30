#!/usr/bin/env bash
# Passo 0: identifica o hardware/firmware do projetor. Não altera nada.
source "$(dirname "$0")/lib.sh"
conectar

DEST="$BACKUPS/$(date +%Y%m%d-%H%M%S)-identificacao"
mkdir -p "$DEST"

for p in ro.product.model ro.product.brand ro.product.device ro.product.board \
         ro.board.platform ro.hardware ro.build.version.release ro.build.version.sdk \
         ro.build.display.id ro.build.flavor ro.build.fingerprint ro.build.date ro.product.cpu.abilist \
         ro.boot.flash.locked ro.boot.verifiedbootstate ro.boot.slot_suffix; do
  printf '%-28s %s\n' "$p" "$(sh_adb getprop "$p")"
done | tee "$DEST/props.txt"

{ echo "device-tree: $(sh_adb 'tr "\\0" " " < /proc/device-tree/compatible')"; sh_adb uname -a; } | tee -a "$DEST/props.txt"
sh_adb cat /proc/meminfo | head -3 | tee -a "$DEST/props.txt"
sh_adb df -h /data | tee -a "$DEST/props.txt"

sh_adb pm list packages -f   | sort > "$DEST/pacotes_todos.txt"
sh_adb pm list packages -s   | sort > "$DEST/pacotes_sistema.txt"
sh_adb pm list packages -3   | sort > "$DEST/pacotes_terceiros.txt"
sh_adb pm list packages -d   | sort > "$DEST/pacotes_desativados.txt"
sh_adb cmd package query-activities -a android.intent.action.MAIN -c android.intent.category.HOME \
  > "$DEST/launchers.txt" 2>/dev/null || true
sh_adb dumpsys activity services > "$DEST/servicos_ativos.txt" 2>/dev/null || true

ok "Relatório salvo em $DEST"
info "Placa: $(id_plataforma | tr '\n' ' ')"
info "Compare com a tabela do README (H713, H726 ou RK3326) antes de seguir."
