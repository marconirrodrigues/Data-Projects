# Pesquisa: quem já otimizou o HY300 Pro

Levantamento de outubro de 2026 no GitHub e na web. **Já existem vários projetos**, mas nenhum junta tudo isto: sem root, reversível, com proteção explícita das funções de hardware e com a lista de apps do usuário. Este repositório consolida as listas deles, ficando com a opção mais conservadora quando as fontes discordam.

## Projetos analisados

| Sigla | Repositório | Placa | Root | Método | Observações |
|---|---|---|---|---|---|
| [M] | [micha102/hy300pro-debloat](https://github.com/micha102/hy300pro-debloat) | Allwinner (H713) | Não | `pm disable-user` em 2 pacotes | Só o malware Hotack. Curto. |
| [P] | [probonopd/hy310-deshittify](https://github.com/probonopd/hy310-deshittify) | H713 (HY310 e similares) | Opcional | `disable.sh` / `enable.sh` via ADB, módulo Magisk, backup FEL | O mais estruturado. Lista testada no firmware `Projector.20250214.153635`. |
| [B] | [battleof3/magcubic-h726-cleanup](https://github.com/battleof3/magcubic-h726-cleanup) | **H726** HY300 Pro | Sim (módulos) | ADB + Magisk no `init_boot`, stubs, patch no `services.jar` | O guia H726 mais completo. Escritas brutas na eMMC = risco alto. |
| [H] | [maximilian-sh/hy350max-badbox-removal](https://github.com/maximilian-sh/hy350max-badbox-removal) | H726 (HY350 Max) | Não | Reempacota o próprio `update.img` | Análise do BADBOX 2.0 e indicadores de comprometimento (IOCs). |
| [X] | [xdawidtech/magcubic-update-and-debloat](https://github.com/xdawidtech/magcubic-update-and-debloat) | Allwinner | Sim | `rm -rf` em `/system`, firmware reempacotado | ⚠️ Remove autofoco, HDMI e proteção térmica. **Não seguir.** |
| [T] | [tqhit/cleanyourprojector](https://github.com/tqhit/cleanyourprojector) | Genérico (Amlogic T950S) | Não | `scan.sh` + `disable.sh` | Boa ferramenta, mas indicadores de outro fabricante. |
| [Y] | [YuujiLab/HY300-H713-Research](https://github.com/YuujiLab/HY300-H713-Research) | H713 | Sim | Pesquisa e dump de firmware | Índice de pesquisa (CC BY-NC-SA). |
| — | [well0nez/magcubic-root](https://github.com/well0nez/magcubic-root) | H713 | Sim | Kit de root + `awimg.py` | README não pôde ser lido. |
| — | [well0nez/allwinner-h713-linux](https://github.com/well0nez/allwinner-h713-linux), [shift/sun50iw12p1-research](https://github.com/shift/sun50iw12p1-research) | H713 | — | Linux mainline no lugar do Android | Experimental, fora do escopo. |
| — | [mdzinh0/hy300-rk3326-clean-rom](https://github.com/mdzinh0/hy300-rk3326-clean-rom), [Hen-Dricks/HY300-Ultimate](https://github.com/Hen-Dricks/HY300-Ultimate), [BruBread/ProjectorRoot](https://github.com/BruBread/ProjectorRoot) | **RK3326** | Sim | ROM limpa / root | Para o HY300 com Rockchip. |
| — | [vipluk/HDMI-Launcher](https://github.com/vipluk/HDMI-Launcher), [AlexisPalacioDev/hy300-poisonos](https://github.com/AlexisPalacioDev/hy300-poisonos), [lquero95/hy300-projector-cleantv](https://github.com/lquero95/hy300-projector-cleantv) | Vários | Não | Launchers alternativos | Ideias para a interface. |

Firmwares de terceiros (androidpctv.com) para [H713](https://androidpctv.com/firmware-magcubic-hy300-hy320/) e [H726](https://androidpctv.com/firmware-magcubic-hy300-pro-ultra-h726/) existem, mas exigem gravar a imagem e podem inutilizar o aparelho se forem da placa errada.

## O que foi encontrado no firmware original

- **Hotack SDK** (`com.hotack.silentsdk`, `com.hotack.writesn`): transforma o projetor em nó de proxy residencial (SOAX). No H726 o payload é o `com.hotack.screensaversdk`.
- **StoreOS** (`com.htc.storeos`): consulta o servidor a cada 5 s e instala APKs em silêncio.
- **OTA por HTTP** (`com.htc.htcotaupdate`, `com.softwinner.update`): reinstala o malware e pode sobrescrever a partição de boot. Por isso é **desativado**, não removido.
- **Toofifi/mphotool** (`com.android.toofifi`, `com.htc.samescreen`): acesso a câmera e microfone, injeção de toques, envio de logs.
- **BADBOX 2.0** em unidades H726 [H].
- Domínios contatados: `store-api.aodintech.com`, `server.mphotool.com`, `saas.zeasn.tv`, `hmma.baidu.com` [B]. Um DNS privado com bloqueio (AdGuard/NextDNS) ajuda a cortar esse tráfego.

A Magcubic [nega que esses APKs sejam malware](https://www.magcubic.com/es/pages/official-statement-regarding-certain-apk-files-on-magcubic-hy300-series-products). As análises acima mostram o comportamento com evidência de rede.

## Onde as fontes discordam (e o que este projeto faz)

| Pacote | Conflito | Decisão aqui |
|---|---|---|
| `com.hysd.vafocus`, `com.htc.closedialog`, `com.softwinner.awsource/awlivetv/TvdVideo/vis/awmanager` | [X] remove; [P] e [B] mantêm | **Protegido** |
| `com.htc.htcbluetoothremotecontrol` | [X] remove se o controle for só IR | **Protegido** |
| `com.mphotool.*`, `com.softwinner.miracastReceiver` | [P] mantém; [B] desativa | Lista opcional |
| `com.android.nfx`, `com.android.ytb` | [B] remove; [X] mantém para Netflix | Lista opcional |
| `com.android.vending` | No H726 o nome é usado por um APK falso ("Tubesky") [H] | Protegido: não mexer pelo nome |
| `com.htc.hyk_test` | Removê-lo faz aparecer a tela de pareamento a cada boot [P] | Só desativar |

## Cuidados

- Nunca apague as partições `Reserve0_a`, `frp` e de armazenamento seguro: guardam calibração, número de série e chaves HDCP [P].
- Reativar um pacote desativado o liga de novo, e a loja do fabricante pode baixar o app outra vez em `/data/app` [P]. Rode `04_debloat.sh` de novo depois de qualquer atualização.
- No H726 com Android 14, o sistema é **32 bits** (`armeabi-v7a`): baixe APKs nessa arquitetura.
