# DAG do Programa Gás do Povo

DAG metodológico (v3) e notebooks de coleta de dados para uma futura avaliação de impacto do **Gás do Povo** (Lei nº 15.348/2026), programa federal de subsídio ao gás de cozinha para famílias de baixa renda inscritas no Cadastro Único.

![DAG v3 — Gás do Povo](dag_gas_do_povo.png)

## Fontes de dados

| Notebook | Fonte | Cobertura | URL |
|----------|-------|-----------|-----|
| `01_download_portal_transparencia.ipynb` | Portal da Transparência / CGU | Pagamentos individuais (nov/2025–, mensal) | https://portaldatransparencia.gov.br/download-de-dados/gas-do-povo |
| `02_download_consolidado_municipio.ipynb` | dados.gov.br / MDS-SAGICAD | Consolidado por município (2021–2025) | https://dados.gov.br/dados/conjuntos-dados/programa-auxilio-gas-dos-brasileiros |
| `03_dag_gas_do_povo.ipynb` | — | DAG metodológico | — |

> **Dados acessados em:** 2026-11-14. As bases são atualizadas mensalmente; verificar data de acesso ao reproduzir análises.

## Estrutura do DAG v3

```
X (caract. pre-trat.) ──► E (elegibilidade) ──► T (voucher) ──► Y (desfecho social)
        │                                            │                  ▲
        └────────────────────────────────────────────│──────────────────┘ (back-door X→Y)
                                                     └──► M (mediadores) ──► Y

U1 (mercado GLP) ─ ─► T e Y    (confundidor latente — borda tracejada)
U2 (fricções acesso) ─ ─► T e Y (confundidor latente — borda tracejada)
```

### Nós (v3)

| Símbolo | Nó | Papel |
|---------|-----|-------|
| **X** | Características pré-tratamento | Confundidor observado: renda per cap., CadÚnico, BPC, chefia feminina, região |
| **E** | Elegibilidade formal | Renda ≤ ½ SM inscrita no CadÚnico (RDD fuzzy no corte) |
| **T** | Gás do Povo (voucher) | Tratamento: recebimento e uso efetivo do voucher |
| **Y** | Desfecho social | Resultado causal: SAN, saúde respiratória, combustível limpo |
| **M** | Mecanismos (mediadores) | Acesso a gás, redução de biomassa, renda domiciliar liberada |
| **U₁** | Mercado local de GLP | Confundidor latente: preço regional, densidade de revendedores |
| **U₂** | Fricções de acesso | Confundidor latente: alfabetização digital, smartphone, distância ao revendedor |

> X→M (pré-tratamento afeta linha de base do uso de biomassa) omitida para clareza visual; relevante em análise de mediação.

## Escopo metodológico

As bases disponíveis permitem estudos **associativos** (cobertura por município × características municipais). Elas **não identificam impacto causal** porque não contêm resultado social externo, grupo contrafactual nem observações anteriores ao programa para o mesmo desfecho.

**Conjunto de ajuste (back-door via X):** `Z = {renda per cap. pré-trat., região, BPC, chefia feminina}` bloqueia o back-door `T ← E ← X → Y` sob Ignorabilidade Condicional. Os confundidores latentes U₁ e U₂ exigem variáveis instrumentais — o preço do petróleo **não é** IV válido para U₁ (viola exclusão via U₁ → Y). Candidatos: distância ao polo de distribuição de GLP ou cobertura de revendedores credenciados pré-programa.

**Quebra estrutural:** Auxílio Gás dos Brasileiros (Lei nº 14.284/2021, depósito bimestral) ≠ Gás do Povo (Lei nº 15.348/2026, voucher mensal). Ao combinar as séries 2021–2026, incluir indicador de fase.

**Unidade de análise:** O DAG é familiar (nível individual). Os dados disponíveis são municipais — risco de falácia ecológica. Em nível municipal, X vira composição (% BPC, % chefia feminina, renda média).

Para uma avaliação de impacto, estratégias recomendadas (com suposição-chave):

| Desenho | Suposição-chave | Estimando |
|---------|-----------------|-----------|
| DiD (escalonado: Callaway-Sant'Anna) | Tendências paralelas | ATT |
| PSM | Ignorabilidade condicional + sobreposição | ATT |
| RDD fuzzy no corte de ½ SM | Continuidade + sem manipulação da renda declarada | LATE |
| IV | Relevância (F > 10) + exclusão + exogeneidade | LATE |

## Arquivos

```
DAG_GAS_DO_POVO_Git/
├── 01_download_portal_transparencia.ipynb   # Download pagamentos (Portal Transparência) — anonimização LGPD incluída
├── 02_download_consolidado_municipio.ipynb  # Download consolidado por município (dados.gov.br)
├── 03_dag_gas_do_povo.ipynb                 # DAG via %run gerar_dag_gas_do_povo.py
├── gerar_dag_gas_do_povo.py                 # Fonte única de verdade do DAG (importado pelo notebook)
├── dag_gas_do_povo.png                      # DAG v3 gerado
├── requirements.txt
└── .gitignore
```

> As pastas `raw/` e `clean/` são criadas em tempo de execução e estão no `.gitignore`.  
> O notebook 01 descarta nome e pseudonimiza CPF (SHA-256) antes de salvar em `clean/` (LGPD).

## Reprodução

```bash
python -m venv .venv
pip install -r requirements.txt
python gerar_dag_gas_do_povo.py
# ou abra os notebooks no Jupyter/VS Code
```
