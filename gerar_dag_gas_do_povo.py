# -*- coding: utf-8 -*-
"""Gera e salva o DAG metodologico v4 do programa Gas do Povo.

Versao 4 — adequacao aos requisitos da atividade (IDP Avaliacao em PP):
- Adiciona no C (Colisor: Recadastramento no CadUnico): X->C<-Y.
  Condicionar em C (ex.: filtrar so familias com cadastro recente)
  abre caminho espurio X<->Y, viesiando estimativas.
- DAG agora cobre todos os requisitos: tratamento, desfecho,
  >= 3 confundidores, 1 mediador e 1 colisor explicitamente rotulado.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from pathlib import Path

DAG_PATH = Path(__file__).resolve().parent / "dag_gas_do_povo.png"

POS = {
    "x":  (1.8,  7.8),   # X: Confundidor observado (pre-tratamento)
    "e":  (5.5,  7.8),   # E: Elegibilidade formal
    "t":  (9.5,  7.8),   # T: Tratamento
    "y":  (13.5, 7.8),   # Y: Desfecho
    "c":  (8.0,  5.5),   # C: COLISOR
    "m":  (12.0, 5.5),   # M: Mediador
    "u1": (4.5,  3.3),   # U1: Confundidor latente
    "u2": (10.0, 3.3),   # U2: Confundidor latente
}

SPECS = {
    "x":  ("X: Caracteristicas Pre-trat.",
           "renda per cap. · BPC · chefia fem. · regiao",
           "#DCEBFA", "#3977A8", False, None),
    "e":  ("E: Elegibilidade Formal",
           "renda <= 1/2 SM · inscrito no CadUnico",
           "#E8F4E8", "#4A9A6A", False, None),
    "t":  ("T: Gas do Povo (voucher)",
           "recebimento e uso do voucher mensal",
           "#DDF3E4", "#378253", False, None),
    "y":  ("Y: Desfecho Social",
           "SAN · saude respiratoria · combustivel limpo",
           "#FADDDD", "#B84D4D", False, None),
    "c":  ("C: Recadastramento CadUnico",
           "COLISOR  (X -> C <- Y)",
           "#FFECF5", "#C04080", False, "COLISOR"),
    "m":  ("M: Mecanismos (Mediador)",
           "acesso a gas · reduc. biomassa · renda liberada",
           "#FFF0C9", "#B78320", False, None),
    "u1": ("U1: Mercado local de GLP",
           "preco regional · cobertura de revendedores",
           "#F5F0FF", "#7663A8", True,  None),
    "u2": ("U2: Friccoes de Acesso",
           "alfab. digital · smartphone · distancia revendedor",
           "#F5F0FF", "#7663A8", True,  None),
}

COL_CONFUND  = "#3977A8"
COL_ELEG     = "#4A9A6A"
COL_TRAT     = "#378253"
COL_MEDIADOR = "#B78320"
COL_COLISOR  = "#C04080"
COL_LATENTE  = "#7663A8"


def desenhar_dag() -> None:
    fig, ax = plt.subplots(figsize=(17, 10), dpi=200)
    fig.patch.set_facecolor("#F7F8FA")
    ax.set_facecolor("#F7F8FA")
    ax.set_xlim(0, 17)
    ax.set_ylim(0, 10)
    ax.axis("off")

    def arrow(a, b, color="#586273", curve=0.0, dashed=False, shrink=50, lw=1.8):
        ax.add_patch(FancyArrowPatch(
            POS[a], POS[b],
            arrowstyle="-|>", mutation_scale=15, linewidth=lw,
            color=color, linestyle="dashed" if dashed else "solid",
            connectionstyle=f"arc3,rad={curve}",
            shrinkA=shrink, shrinkB=shrink, zorder=2,
        ))

    # Cadeia causal principal
    arrow("x", "e",  color=COL_CONFUND)
    arrow("x", "y",  color=COL_CONFUND, curve=-0.13, shrink=38)   # back-door
    arrow("e", "t",  color=COL_ELEG)
    arrow("t", "y",  color=COL_TRAT)
    arrow("t", "m",  color=COL_MEDIADOR)
    arrow("m", "y",  color=COL_MEDIADOR, curve=-0.12)

    # Colisor: X->C e Y->C (arestas convergem em C)
    arrow("x", "c",  color=COL_COLISOR, curve= 0.10, shrink=42, lw=2.0)
    arrow("y", "c",  color=COL_COLISOR, curve=-0.10, shrink=42, lw=2.0)

    # Confundidores latentes
    arrow("u1", "t",  color=COL_LATENTE, dashed=True, curve= 0.18, shrink=45)
    arrow("u1", "y",  color=COL_LATENTE, dashed=True, curve=-0.08, shrink=45)
    arrow("u2", "t",  color=COL_LATENTE, dashed=True, curve=-0.15, shrink=45)
    arrow("u2", "y",  color=COL_LATENTE, dashed=True, curve= 0.12, shrink=45)

    # Nos
    BOX_W = 3.3
    for key, (title, subtitle, fill, edge, latente, tag) in SPECS.items():
        x, y = POS[key]
        ls = (0, (5, 3)) if latente else "solid"
        lw_box = 2.2 if tag == "COLISOR" else 1.7
        ax.add_patch(FancyBboxPatch(
            (x - BOX_W / 2, y - 0.55), BOX_W, 1.1,
            boxstyle="round,pad=0.06,rounding_size=0.12",
            facecolor=fill, edgecolor=edge, linewidth=lw_box,
            linestyle=ls, zorder=3,
        ))
        ax.text(x, y + 0.15, title, ha="center", va="center",
                fontsize=9.5, fontweight="bold", color="#172033", zorder=4)
        ax.text(x, y - 0.21, subtitle, ha="center", va="center",
                fontsize=7.5, color="#4B5563", zorder=4)
        if tag == "COLISOR":
            ax.text(x, y + 0.50, "COLISOR", ha="center", va="center",
                    fontsize=8.5, fontweight="bold", color=COL_COLISOR,
                    zorder=4,
                    bbox=dict(boxstyle="round,pad=0.15", facecolor="#FFD6EB",
                              edgecolor=COL_COLISOR, linewidth=1.0))

    # Titulo
    ax.text(8.5, 9.58, "DAG v4 — Gas do Povo: Avaliacao de Impacto",
            fontsize=19, fontweight="bold", color="#172033", ha="center")
    ax.text(8.5, 9.14,
            "C = colisor  |  E = elegibilidade (RDD fuzzy)  |"
            "  nos U = confundidores latentes (borda tracejada)",
            fontsize=10, color="#536074", ha="center")

    # Nota metodologica
    note = (
        "CONTROLAR (back-door via X): Z = {renda per cap., regiao, BPC, chefia feminina}"
        " bloqueia T<-E<-X->Y. U1 e U2 exigem IV.\n"
        "NAO CONTROLAR por C (colisor): condicionar em C abre caminho espurio X<->Y"
        " (selecao de amostras com 'cadastro atualizado' vicia a estimativa).\n"
        "MEDIADOR M: nao controlar por M para estimar efeito total de T->Y;"
        " controlar apenas em analise de mediacao (efeito direto/indireto).\n"
        "QUEBRA ESTRUTURAL: Auxilio Gas (Lei 14.284/2021) != Gas do Povo (Lei 15.348/2026)."
        " Inclua indicador de fase ao combinar as series.\n"
        "SUTVA: voucher em massa pode alterar preco local (T->U1 — spillover)."
        " RDD no corte de 1/2 SM e fuzzy (E != T)."
    )
    ax.text(0.3, 1.9, note, fontsize=8.8, color="#7A4D11", ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.55", facecolor="#FFF7E3",
                      edgecolor="#D7A94E", linewidth=1.3))

    # Legenda
    legend_items = [
        mpatches.Patch(facecolor="#DCEBFA", edgecolor=COL_CONFUND,
                       label="X: Confundidor observado (pre-tratamento)"),
        mpatches.Patch(facecolor="#E8F4E8", edgecolor=COL_ELEG,
                       label="E: Elegibilidade formal"),
        mpatches.Patch(facecolor="#DDF3E4", edgecolor=COL_TRAT,
                       label="T: Tratamento — voucher Gas do Povo"),
        mpatches.Patch(facecolor="#FADDDD", edgecolor="#B84D4D",
                       label="Y: Desfecho social"),
        mpatches.Patch(facecolor="#FFECF5", edgecolor=COL_COLISOR,
                       label="C: COLISOR — nao controlar"),
        mpatches.Patch(facecolor="#FFF0C9", edgecolor=COL_MEDIADOR,
                       label="M: Mediador pos-tratamento"),
        mpatches.Patch(facecolor="#F5F0FF", edgecolor=COL_LATENTE,
                       label="U: Confundidor latente (nao observado)"),
    ]
    ax.legend(handles=legend_items, loc="lower right", fontsize=8.3,
              framealpha=0.90, edgecolor="#CCCCCC",
              bbox_to_anchor=(0.99, 0.01))

    plt.savefig(DAG_PATH, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"DAG v4 salvo em: {DAG_PATH}")


if __name__ == "__main__":
    desenhar_dag()
