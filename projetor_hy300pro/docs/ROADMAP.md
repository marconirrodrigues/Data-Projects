# Roteiro

## Fase 1: diagnóstico (agora)
- [ ] Rodar `00_identificar.sh` e anotar placa, firmware (`ro.build.display.id`) e RAM
- [ ] Rodar `01_backup.sh`
- [ ] Conferir `pacotes_sistema.txt` contra `config/remover.d/` e acrescentar pacotes suspeitos que só existam no meu firmware
- [ ] Medir o "antes": tempo de boot, RAM livre (`dumpsys meminfo`), tempo para abrir Netflix/YouTube

## Fase 2: limpeza sem root
- [x] Escolher os apps em `config/apps.conf`: Netflix, YouTube, Prime Video, Globoplay e VLC
- [ ] Baixar os APKs (versão Android TV, `armeabi-v7a`) para `apks/`
- [ ] Instalar o Cinema e o Projectivy e definir o Cinema como launcher padrão
- [ ] `LISTAS="malware"` → testar → `LISTAS="malware bloat"` → testar
- [ ] Checklist de funções após cada passo: autofoco, keystone, zoom, HDMI, controle IR/BT, Wi-Fi, Bluetooth, som, espelhamento (se usar), desligamento por temperatura
- [ ] Medir o "depois" e registrar aqui

## Fase 3: interface (launcher Cinema)
- [x] v0.1: destaque do app em foco, dock de vidro com zoom, atalhos de HDMI/imagem/foco/ajustes, grade de todos os apps
- [ ] Primeiro APK pelo GitHub Actions e teste no aparelho
- [ ] Ajustar tamanhos à densidade real da tela (`adb shell wm density`)
- [ ] Confirmar as activities de keystone e foco do firmware 20250117 (`dumpsys package com.htc.magcubicos`)
- [ ] "Continuar assistindo" no destaque (canais do Android TV), se o desempenho permitir
- [ ] Papel de parede próprio e tema claro/escuro
- [ ] Projectivy instalado como launcher reserva

## Fase 4: manutenção
- [ ] Bloquear atualizações OTA do fabricante (já desativadas) e reaplicar o debloat se algo voltar
- [ ] Script de verificação periódica: avisar se algum pacote da lista de malware reaparecer

## Fora do escopo (por enquanto)
- Root, Magisk, gravar firmware ou Linux mainline: ganho pequeno para o risco de inutilizar o aparelho.
