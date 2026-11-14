# -*- coding: utf-8 -*-
"""Gera e salva o DAG metodológico v2 do programa Gás do Povo.

Correções v2:
- Removido nó operacional 'dados': não é variável do DGP (Pearl 2009).
- Adicionados confundidores latentes U1 (mercado GLP) e U2 (fricções de acesso).
- Corrigida ambiguidade de rótulo 'renda' em três nós com papéis causais distintos.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from pathlib import Path

DAG_PATH = Path(__file__).resolve().parent / "dag_gas_do_povo.png"

POS = {
    "cad":    (2.5,  7.8),
    "gdp":    (8.0,  7.8),
    "out":    (13.5, 7.8),
    "mech":   (10.8, 5.5),
    "u_mkt":  (5.0,  3.5),
    "u_fric": (10.5, 3.5),
}

SPECS = {
    "cad":    ("X: Elegibilidade Pré-tratamento",
               "CadÚnico · renda per capita pré-trat. · BPC · chefia feminina",
               "#DCEBFA", "#3977A8", False),
    "gdp":    ("T: Gás do Povo (voucher)",
               "recebimento e uso do voucher mensal de gás",
               "#DDF3E4", "#378253", False),
    "out":    ("Y: Desfecho Social (pós-programa)",
               "SAN · saúde respiratória · combustível limpo",
               "#FADDDD", "#B84D4D", False),
    "mech":   ("M: Mecanismos (Mediadores)",
               "acesso a gás · ↓ biomassa · renda domiciliar liberada",
               "#FFF0C9", "#B78320", False),
    "u_mkt":  ("U₁: Mercado local de GLP",
               "preço regional · densidade de revendedores credenciados",
               "#F5F0FF", "#7663A8", True),
    "u_fric": ("U₂: Fricções de Acesso",
               "alfabetização digital · smartphone · distância ao revendedor",
               "#F5F0FF", "#7663A8", True),
}


def desenhar_dag() -> None:
    fig, ax = plt.subplots(figsize=(16, 10), dpi=200)
    fig.patch.set_facecolor("#F7F8FA")
    ax.set_facecolor("#F7F8FA")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis("off")

    def arrow(a, b, color="#586273", curve=0.0, dashed=False, shrink=78):
        ax.add_patch(FancyArrowPatch(
            POS[a], POS[b],
            arrowstyle="-|>", mutation_scale=16, linewidth=2.0,
            color=color, linestyle="dashed" if dashed else "solid",
            connectionstyle=f"arc3,rad={curve}",
            shrinkA=shrink, shrinkB=shrink, zorder=1,
        ))

    arrow("cad",    "gdp",   color="#3977A8")
    arrow("cad",    "out",   color="#3977A8", curve=-0.15)
    arrow("gdp",    "out",   color="#378253")
    arrow("gdp",    "mech",  color="#B78320")
    arrow("mech",   "out",   color="#B78320", curve=-0.10)
    arrow("u_mkt",  "gdp",   color="#7663A8", dashed=True, curve= 0.15)
    arrow("u_mkt",  "out",   color="#7663A8", dashed=True, curve=-0.10)
    arrow("u_fric", "gdp",   color="#7663A8", dashed=True, curve=-0.10)

    for key, (title, subtitle, fill, edge, latente) in SPECS.items():
        x, y = POS[key]
        ls = (0, (5, 3)) if latente else "solid"
        ax.add_patch(FancyBboxPatch(
            (x - 2.1, y - 0.56), 4.2, 1.12,
            boxstyle="round,pad=0.06,rounding_size=0.13",
            facecolor=fill, edgecolor=edge, linewidth=1.7,
            linestyle=ls, zorder=3,
        ))
        ax.text(x, y + 0.16, title, ha="center", va="center",
                fontsize=10.5, fontweight="bold", color="#172033", zorder=4)
        ax.text(x, y - 0.21, subtitle, ha="center", va="center",
                fontsize=8.0, color="#4B5563", zorder=4)

    ax.text(7.9, 9.55,
            "DAG v2 — Avaliação de Impacto do Gás do Povo",
            fontsize=20, fontweight="bold", color="#172033", ha="center")
    ax.text(7.9, 9.10,
            "Resultado deve ser externo ao voucher · nós U = confundidores latentes (borda tracejada)",
            fontsize=10.5, color="#536074", ha="center")

    note = (
        "ANÁLISE DISPONÍVEL AGORA  •  As bases atuais permitem estudos associativos. "
        "Não há resultado social externo nem contrafactual.\n"
        "DADOS NECESSÁRIOS para identificação causal: painel município × ano, desfecho externo (SAN/saúde), "
        "proxy para U₁ (preço local GLP) e U₂ (acesso digital).\n"
        "QUEBRA ESTRUTURAL: Auxílio Gás dos Brasileiros (Lei 14.284/2021) ≠ Gás do Povo (Lei 15.348/2026). "
        "Inclua indicador de fase ao combinar as séries.\n"
        "CONJUNTO DE AJUSTE (back-door): Z = {renda per capita pré-trat., região, BPC, chefia feminina}. "
        "U₁ e U₂ exigem variáveis instrumentais."
    )
    ax.text(0.4, 1.9, note, fontsize=9.2, color="#7A4D11", ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.6", facecolor="#FFF7E3",
                      edgecolor="#D7A94E", linewidth=1.3))

    legend_items = [
        mpatches.Patch(facecolor="#DCEBFA", edgecolor="#3977A8",
                       label="X: Elegibilidade pré-tratamento (observado)"),
        mpatches.Patch(facecolor="#DDF3E4", edgecolor="#378253",
                       label="T: Tratamento — Gás do Povo (observado)"),
        mpatches.Patch(facecolor="#FADDDD", edgecolor="#B84D4D",
                       label="Y: Desfecho social externo (observado)"),
        mpatches.Patch(facecolor="#FFF0C9", edgecolor="#B78320",
                       label="M: Mediadores pós-tratamento (observado)"),
        mpatches.Patch(facecolor="#F5F0FF", edgecolor="#7663A8",
                       label="U: Confundidor latente (não observado)"),
    ]
    ax.legend(handles=legend_items, loc="lower right", fontsize=9,
              framealpha=0.90, edgecolor="#CCCCCC",
              bbox_to_anchor=(0.99, 0.01))

    plt.savefig(DAG_PATH, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"DAG v2 salvo em: {DAG_PATH}")


if __name__ == "__main__":
    desenhar_dag()
