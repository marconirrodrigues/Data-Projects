# Meu aparelho

Dados da tela **Configurações > Sobre o dispositivo** (número de série e MAC omitidos de propósito).

| Item | Valor |
|---|---|
| Modelo | HY300Pro |
| Android | 11 |
| Firmware | `UL_Veng.projector.20250117.194417` |
| RAM total / livre | 1 GB / 410,9 MB (com o sistema original, sem otimização) |
| Armazenamento total / livre | 8 GB / 3,67 GB |

## Conclusão

Android 11 com 1 GB/8 GB é a versão **Allwinner H713** (`sun50iw12p1`), a mais estudada pela comunidade.
Portanto:

- As listas de `config/remover.d/` se aplicam, incluindo o malware Hotack (`com.hotack.silentsdk`).
- O ADB por Wi-Fi (`IP:5555`) deve funcionar.
- O launcher original provavelmente é o malicioso `com.htc.htclauncherhighenglishd08`: instale o Projectivy **antes** do debloat.
- O firmware `20250117` é **anterior** aos testados por outros projetos (`20250214` e `20250724`): rode o debloat em simulação primeiro e compare com `pacotes_sistema.txt`.
- Confirmar a placa com `00_identificar.sh` (esperado: `sun50iw12` / `h713`).

## Medições

| Momento | RAM livre | Armazenamento livre | Boot (s) | Observações |
|---|---|---|---|---|
| Original | 410,9 MB | 3,67 GB | | foto da tela Sobre |
| Após malware | | | | |
| Após bloat | | | | |
