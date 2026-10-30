# Roteiro

## Fase 1: diagnóstico (agora)
- [ ] Rodar `00_identificar.sh` e anotar placa, firmware (`ro.build.display.id`) e RAM
- [ ] Rodar `01_backup.sh`
- [ ] Conferir `pacotes_sistema.txt` contra `config/remover.d/` e acrescentar pacotes suspeitos que só existam no meu firmware
- [ ] Medir o "antes": tempo de boot, RAM livre (`dumpsys meminfo`), tempo para abrir Netflix/YouTube

## Fase 2: limpeza sem root
- [ ] Escolher os apps em `config/apps.conf` e baixar os APKs para `apks/`
- [ ] Instalar o Projectivy e definir como launcher padrão
- [ ] `LISTAS="malware"` → testar → `LISTAS="malware bloat"` → testar
- [ ] Checklist de funções após cada passo: autofoco, keystone, zoom, HDMI, controle IR/BT, Wi-Fi, Bluetooth, som, espelhamento (se usar), desligamento por temperatura
- [ ] Medir o "depois" e registrar aqui

## Fase 3: interface
- [ ] Configurar o Projectivy: só os apps desejados, atalho direto para a entrada HDMI, papel de parede, ocultar o resto
- [ ] Avaliar um launcher próprio (ver HDMI-Launcher e PoisonOS na pesquisa) se o Projectivy não bastar

## Fase 4: manutenção
- [ ] Bloquear atualizações OTA do fabricante (já desativadas) e reaplicar o debloat se algo voltar
- [ ] Script de verificação periódica: avisar se algum pacote da lista de malware reaparecer

## Fora do escopo (por enquanto)
- Root, Magisk, gravar firmware ou Linux mainline: ganho pequeno para o risco de inutilizar o aparelho.
