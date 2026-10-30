#!/usr/bin/env bash
# Passo 2: instala os APKs colocados na pasta apks/ (um .apk ou uma pasta por app, para split APKs).
source "$(dirname "$0")/lib.sh"
conectar
exigir_backup

shopt -s nullglob
for item in "$RAIZ"/apks/*; do
  if [[ -d "$item" ]]; then
    partes=("$item"/*.apk)
    (( ${#partes[@]} )) || continue
    adb install-multiple -r "${partes[@]}" && ok "Instalado: $(basename "$item")"
  elif [[ "$item" == *.apk ]]; then
    adb install -r "$item" && ok "Instalado: $(basename "$item")"
  fi
done
