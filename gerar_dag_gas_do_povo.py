# -*- coding: utf-8 -*-
"""Gera e salva o DAG metodologico v3 do programa Gas do Povo.

Versao 3 — correcoes apos segunda auditoria:
- Adiciona no E (Elegibilidade formal): distingue elegibilidade do
  recebimento/uso do voucher, tornando o RDD fuzzy explicito.
- Adiciona aresta U2->Y: friccoes de acesso afetam SAN por outras
  vias (exclusao digital correlaciona com inseguranca alimentar),
  tornando U2 confundidor verdadeiro, nao candidato a instrumento.
- Corrige rotulo da tabela de interpretacao: T<-X->Y e back-door,
  nao X->T->Y.
- Remove sugestao de preco do petroleo como IV para U1 (viola
  exclusao: petroleo -> U1 -> Y). Propoe distancia ao polo de
  distribuicao e cobertura pre-programa como candidatos.
- Adiciona nota sobre SUTVA/spillovers (T->U1 pode ocorrer em escala)
  e sobre X->M omitida para clareza visual.
- Reduz shrink de 78 para 50, adequado para nos adjacentes.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from pathlib import Path

DAG_PATH = Path(__file__).resolve().parent / "dag_gas_do_povo.png"

# Cadeia principal (linha superior): X -> E -> T -> Y
# Mediador (linha intermediaria): M
# Confundidores latentes (linha inferior): U1, U2
POS = {
    "x":  (1.8,  7.8),   # X: Caracteristicas pre-tratamento (observado)
    "e":  (5.5,  7.8),   # E: Elegibilidade formal (observado)
    "t":  (9.5,  7.8),   # T: Recebimento/uso do voucher (observado)
    "y":  (13.5, 7.8),   # Y: Desfecho social (nao observado nas bases atuais)
    "m":  (11.5, 5.4),   # M: Mecanismos mediadores (observado)
    "u1": (4.5,  3.4),   # U1: Mercado local de GLP (nao observado)
    "u2": (10.0, 3.4),   # U2: Friccoes de acesso (nao observado)
}

SPECS = {
    "x":  ("X: Caracteristicas Pre-trat.",
           "CadUnico · renda per cap. · BPC · chefia fem. · regiao",
           "#DCEBFA", "#3977A8", False),
    "e":  ("E: Elegibilidade Formal",
           "renda <= 1/2 SM · inscrito no CadUnico",
           "#E8F4E8", "#4A9A6A", False),
    "t":  ("T: Gas do Povo (voucher)",
           "recebimento e uso do voucher mensal",
           "#DDF3E4", "#378253", False),
    "y":  ("Y: Desfecho Social",
           "SAN · saude respiratoria · combustivel limpo",
           "#FADDDD", "#B84D4D", False),
    "m":  ("M: Mecanismos (Mediadores)",
           "acesso a gas · reduc. biomassa · renda liberada",
           "#FFF0C9", "#B78320", False),
    "u1": ("U1: Mercado local de GLP",
           "preco regional · cobertura de revendedores",
           "#F5F0FF", "#7663A8", True),
    "u2": ("U2: Friccoes de Acesso",
           "alfab. digital · smartphone · distancia ao revendedor",
           "#F5F0FF", "#7663A8", True),
}


def desenhar_dag() -> None:
    fig, ax = plt.subplots(figsize=(16, 10), dpi=200)
    fig.patch.set_facecolor("#F7F8FA")
    ax.set_facecolor("#F7F8FA")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis("off")

    def arrow(a, b, color="#586273", curve=0.0, dashed=False, shrink=50):
        ax.add_patch(FancyArrowPatch(
            POS[a], POS[b],
            arrowstyle="-|>", mutation_scale=15, linewidth=1.8,
            color=color, linestyle="dashed" if dashed else "solid",
            connectionstyle=f"arc3,rad={curve}",
            shrinkA=shrink, shrinkB=shrink, zorder=2,
        ))

    # Cadeia principal observada
    arrow("x",  "e",  color="#3977A8")
    arrow("x",  "y",  color="#3977A8", curve=-0.12, shrink=40)  # back-door X->Y
    arrow("e",  "t",  color="#4A9A6A")
    arrow("t",  "y",  color="#378253")
    arrow("t",  "m",  color="#B78320")
    arrow("m",  "y",  color="#B78320", curve=-0.10)

    # Confundidores latentes (tracejado)
    arrow("u1", "t",  color="#7663A8", dashed=True, curve= 0.18, shrink=45)
    arrow("u1", "y",  color="#7663A8", dashed=True, curve=-0.08, shrink=45)
    arrow("u2", "t",  color="#7663A8", dashed=True, curve=-0.15, shrink=45)
    arrow("u2", "y",  color="#7663A8", dashed=True, curve= 0.12, shrink=45)

    # Nos
    BOX_W = 3.4
    for key, (title, subtitle, fill, edge, latente) in SPECS.items():
        x, y = POS[key]
        ls = (0, (5, 3)) if latente else "solid"
        ax.add_patch(FancyBboxPatch(
            (x - BOX_W / 2, y - 0.55), BOX_W, 1.1,
            boxstyle="round,pad=0.06,rounding_size=0.12",
            facecolor=fill, edgecolor=edge, linewidth=1.7,
            linestyle=ls, zorder=3,
        ))
        ax.text(x, y + 0.15, title, ha="center", va="center",
                fontsize=9.8, fontweight="bold", color="#172033", zorder=4)
        ax.text(x, y - 0.21, subtitle, ha="center", va="center",
                fontsize=7.8, color="#4B5563", zorder=4)

    # Titulo
    ax.text(8.0, 9.55, "DAG v3 — Gas do Povo: Avaliacao de Impacto",
            fontsize=19, fontweight="bold", color="#172033", ha="center")
    ax.text(8.0, 9.12,
            "E = elegibilidade (RDD fuzzy no corte de 1/2 SM)  |"
            "  nos U = confundidores latentes (borda tracejada)",
            fontsize=10, color="#536074", ha="center")

    # Nota metodologica compacta
    note = (
        "ANALISE DISPONIVEL: Estudos associativos (cobertura x caracteristicas municipais)."
        "  Sem desfecho externo nem contrafactual nas bases atuais.\n"
        "IDENTIFICACAO CAUSAL: Painel municipio x ano + desfecho externo (SAN/saude)"
        " + proxy para U1 (distancia ao polo GLP, cobertura pre-programa) e U2 (acesso digital).\n"
        "AJUSTE (back-door via X): Z = {renda per cap. pre-trat., regiao, BPC, chefia feminina}"
        " bloqueia T<-E<-X->Y."
        "  U1 e U2 exigem IV; preco do petroleo NAO e IV valido (viola exclusao via U1->Y).\n"
        "QUEBRA ESTRUTURAL: Auxilio Gas (Lei 14.284/2021) != Gas do Povo (Lei 15.348/2026)."
        "  Inclua indicador de fase ao combinar as series.\n"
        "SUTVA/X->M: Voucher em massa pode alterar preco local (T->U1 — spillover)."
        "  X->M (pre-trat. afeta biomassa) omitida para clareza; relevante em analise de mediacao."
    )
    ax.text(0.3, 1.9, note, fontsize=8.8, color="#7A4D11", ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.55", facecolor="#FFF7E3",
                      edgecolor="#D7A94E", linewidth=1.3))

    # Legenda
    legend_items = [
        mpatches.Patch(facecolor="#DCEBFA", edgecolor="#3977A8",
                       label="X: Caract. pre-tratamento (observado)"),
        mpatches.Patch(facecolor="#E8F4E8", edgecolor="#4A9A6A",
                       label="E: Elegibilidade formal (observado)"),
        mpatches.Patch(facecolor="#DDF3E4", edgecolor="#378253",
                       label="T: Tratamento — voucher (observado)"),
        mpatches.Patch(facecolor="#FADDDD", edgecolor="#B84D4D",
                       label="Y: Desfecho social (nao observado nas bases atuais)"),
        mpatches.Patch(facecolor="#FFF0C9", edgecolor="#B78320",
                       label="M: Mediadores pos-tratamento (observado)"),
        mpatches.Patch(facecolor="#F5F0FF", edgecolor="#7663A8",
                       label="U: Confundidor latente (nao observado)"),
    ]
    ax.legend(handles=legend_items, loc="lower right", fontsize=8.5,
              framealpha=0.90, edgecolor="#CCCCCC",
              bbox_to_anchor=(0.99, 0.01))

    plt.savefig(DAG_PATH, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"DAG v3 salvo em: {DAG_PATH}")


if __name__ == "__main__":
    desenhar_dag()
