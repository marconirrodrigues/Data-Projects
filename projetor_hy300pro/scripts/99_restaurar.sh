#!/usr/bin/env bash
# Desfaz o debloat: reinstala/reativa pacotes para o usuário 0.
#   ./scripts/99_restaurar.sh 192.168.0.50 com.pacote.x            -> um pacote
#   LOG=backups/xxx-debloat.log ./scripts/99_restaurar.sh 192...   -> tudo de um log
source "$(dirname "$0")/lib.sh"
conectar

if [[ -n "${LOG:-}" ]]; then
  pacotes="$(awk '{print $2}' "$LOG")"
else
  pacotes="${2:?Informe o pacote ou LOG=arquivo.log}"
fi

for pkg in $pacotes; do
  sh_adb cmd package install-existing --user 0 "$pkg" >/dev/null 2>&1 || true
  sh_adb pm enable --user 0 "$pkg" >/dev/null 2>&1 || true
  instalado "$pkg" && ok "Restaurado: $pkg" || aviso "Não restaurado: $pkg"
done
