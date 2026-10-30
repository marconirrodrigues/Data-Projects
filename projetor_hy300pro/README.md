# projetor_hy300pro

Otimização do projetor **Magcubic HY300 Pro**: remover malware e bloatware, trocar a interface por um launcher limpo e deixar só os apps que eu quero, **sem perder nenhuma função do projetor** (autofoco, keystone, HDMI, controle remoto, proteção térmica).

Tudo é feito via **ADB, sem root e de forma reversível**: os pacotes são desativados/removidos só para o usuário 0, a partição `/system` não é alterada e qualquer mudança volta com `scripts/99_restaurar.sh`.

> ⚠️ Use por sua conta e risco. Os passos sem root deste projeto não gravam firmware e são reversíveis, mas teste um passo de cada vez.

## 1. Primeiro: qual HY300 Pro você tem?

"HY300 Pro" é vendido com placas diferentes. As listas deste projeto valem para **Allwinner H713 e H726**. O HY300 com **Rockchip RK3326** é outro aparelho: não use estas listas nele (ver `docs/PESQUISA.md`).

| Placa | Android | Como reconhecer (`00_identificar.sh`) | ADB por Wi-Fi |
|---|---|---|---|
| Allwinner **H713** | 11 | `sun50iw12`, flavor `h713_tuna_p3` | funciona (`IP:5555`) |
| Allwinner **H726** | 14 | `sun50iw15` / `hermes`, flavor `h726_p2` | costuma falhar: use cabo USB |
| Rockchip **RK3326** | 8.1 | `rk3326`, `rk30board` | fora do escopo |

## 2. Preparação

1. Instale o [Android platform-tools](https://developer.android.com/tools/releases/platform-tools) (`adb`) no PC.
2. No projetor: **Configurações > Sobre**, aperte OK no nome do modelo 7 a 10 vezes para liberar as Opções do desenvolvedor, depois ative **Depuração ADB/USB**.
3. Conecte pelo cabo USB ou pela rede (`./scripts/00_identificar.sh 192.168.0.50`) e aceite "Sempre permitir" na tela.
4. Ao terminar, **desligue a depuração**: ADB aberto na rede dá acesso total ao aparelho.

## 3. Passo a passo

Todos os scripts aceitam o IP do projetor como 1º argumento (ou `HY300_IP=...`). Sem IP, usam o USB.

| # | Script | O que faz | Altera algo? |
|---|---|---|---|
| 0 | `00_identificar.sh` | Placa, firmware, RAM e lista de pacotes em `backups/` | Não |
| 1 | `01_backup.sh` | Lista de pacotes, configurações e APKs instalados | Não |
| 2 | `02_instalar_apps.sh` | Instala os APKs que você colocou em `apks/` | Sim |
| 3 | `03_otimizar.sh` | Animações 0.5x, launcher padrão, DNS privado opcional, limpeza de cache | Sim (reversível) |
| 4 | `04_debloat.sh` | Desativa malware e bloat das listas em `config/remover.d/` | Sim (reversível) |
| ↩ | `99_restaurar.sh` | Reativa pacotes a partir do log do debloat | Desfaz o passo 4 |

Exemplo completo:

```bash
./scripts/00_identificar.sh 192.168.0.50
./scripts/01_backup.sh 192.168.0.50
./scripts/02_instalar_apps.sh 192.168.0.50              # Projectivy + seus apps
LAUNCHER=com.spocky.projengmenu DNS_PRIVADO=dns.adguard-dns.com \
  ./scripts/03_otimizar.sh 192.168.0.50
./scripts/04_debloat.sh 192.168.0.50                    # simulação: só mostra o que faria
APLICAR=1 ./scripts/04_debloat.sh 192.168.0.50          # aplica (pm disable-user)
# reinicie e teste foco, keystone, HDMI, controle, Wi-Fi e som

# Se algo quebrar:
LOG=backups/AAAAMMDD-HHMMSS-debloat.log ./scripts/99_restaurar.sh 192.168.0.50
```

Opções do debloat:

- `LISTAS="malware"`: só remove o malware. O padrão é `"malware bloat"`. Acrescente `opcional` para espelhamento de tela, helpers de Netflix/YouTube e módulos de anúncios do AOSP.
- `MODO=remover`: usa `pm uninstall --user 0` em vez de desativar. Só depois de testar o modo desativar. Itens marcados `:desativar` nunca são desinstalados.
- `FORCAR=1`: roda numa placa fora de `config/plataformas.txt`. Não use sem conferir os pacotes.

## 4. Configuração

| Arquivo | Para que serve |
|---|---|
| `config/apps.conf` | Apps que eu quero. Eles também ficam protegidos contra o debloat. |
| `config/proteger.txt` | Pacotes de hardware que **nunca** são tocados: foco, keystone, HDMI, controle, térmico, Configurações |
| `config/remover.d/10-malware.txt` | Hotack (proxy SOAX), StoreOS, OTA inseguro, telemetria, pilha de cast Toofifi |
| `config/remover.d/20-bloat.txt` | Apps inúteis no projetor (Office, galeria, impressão, temas etc.) |
| `config/remover.d/30-opcional.txt` | Só entra se você pedir |
| `config/plataformas.txt` | Placas onde as listas foram validadas |

## 5. Launcher (interface)

Recomendado: **Projectivy Launcher** (`com.spocky.projengmenu`), feito para projetores e usado pelos outros projetos de debloat. No H726 baixe a variante `armeabi-v7a` (o sistema é 32 bits) e confira a assinatura (`CN=Despesse Mickael`).

Instale o novo launcher **antes** do debloat: em unidades H713 o launcher original (`com.htc.htclauncherhighenglishd08`) é malicioso e será desativado. O `com.htc.magcubicos` (keystone/projeção) continua instalado; a entrada HDMI pode ser aberta pelo atalho do `com.softwinner.awlivetv`.

## 6. Roteiro

Ver [`docs/ROADMAP.md`](docs/ROADMAP.md). Pesquisa e fontes: [`docs/PESQUISA.md`](docs/PESQUISA.md). Dados do meu projetor (H713, Android 11): [`docs/MEU_APARELHO.md`](docs/MEU_APARELHO.md).
