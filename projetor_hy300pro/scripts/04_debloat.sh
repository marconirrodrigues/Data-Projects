#!/usr/bin/env bash
# Passo 4: desativa/remove para o usuário 0 os pacotes de config/remover.d/.
# Nada é apagado da partição /system: tudo volta com 99_restaurar.sh.
#
#   ./scripts/04_debloat.sh                          -> simulação via USB (não altera nada)
#   APLICAR=1 ./scripts/04_debloat.sh                -> aplica (pm disable-user)
#   MODO=remover APLICAR=1 ./scripts/04_debloat.sh   -> pm uninstall --user 0 (após testar)
#   LISTAS="malware" ...                             -> só algumas listas (padrão: malware bloat)
source "$(dirname "$0")/lib.sh"
conectar
checar_plataforma
exigir_backup

APLICAR="${APLICAR:-0}"
MODO="${MODO:-desativar}"
LISTAS="${LISTAS:-malware bloat}"
LOG="$BACKUPS/$(date +%Y%m%d-%H%M%S)-debloat.log"
mkdir -p "$BACKUPS"

[[ "$APLICAR" == "1" ]] || aviso "SIMULAÇÃO: nada será alterado. Use APLICAR=1 para aplicar."

for nome in $LISTAS; do
  arquivo="$(ls "$CONFIG"/remover.d/*-"$nome".txt 2>/dev/null | head -1)"
  [[ -n "$arquivo" ]] || erro "Lista não encontrada: $nome"
  info "Lista: $(basename "$arquivo")"

  while read -r pkg forcar; do
    if protegido "$pkg"; then
      aviso "Ignorado (protegido): $pkg"; continue
    fi
    instalado "$pkg" || continue

    acao="${forcar:-$MODO}"
    if [[ "$APLICAR" != "1" ]]; then
      info "Seria $acao: $pkg"; continue
    fi
    sh_adb am force-stop "$pkg" >/dev/null || true
    if [[ "$acao" == "remover" ]]; then
      saida="$(sh_adb pm uninstall -k --user 0 "$pkg" || true)"
    else
      saida="$(sh_adb pm disable-user --user 0 "$pkg" || true)"
    fi
    echo "$acao $pkg :: $saida" | tee -a "$LOG"
  done < <(ler_lista_modo "$arquivo")
done

if [[ "$APLICAR" == "1" ]]; then
  ok "Log salvo em $LOG (use com: LOG=$LOG ./scripts/99_restaurar.sh)"
  aviso "Espere ~10 s antes de reiniciar. Depois teste: foco, keystone, HDMI, controle, Wi-Fi e som."
fi
