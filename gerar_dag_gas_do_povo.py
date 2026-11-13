# -*- coding: utf-8 -*-
"""Gera e salva o DAG metodológico do programa Gás do Povo."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from pathlib import Path

DAG_PATH = Path(__file__).resolve().parent / "dag_gas_do_povo.png"

POS = {
    "cad":   (2.5,  6.5),
    "gdp":   (8.0,  6.5),
    "out":   (13.5, 6.5),
    "mech":  (10.8, 3.8),
    "dados": (5.2,  3.8),
}

SPECS = {
    "cad":   ("Características prévias",
              "CadÚnico · renda · BPC · chefia feminina · região",
              "#DCEBFA", "#3977A8"),
    "gdp":   ("Gás do Povo",
              "tratamento: recebimento do voucher de gás",
              "#DDF3E4", "#378253"),
    "out":   ("Resultado social externo",
              "SAN · saúde · renda · combustível limpo",
              "#FADDDD", "#B84D4D"),
    "mech":  ("Mecanismos pós-programa",
              "acesso a gás · redução de biomassa · renda disponível",
              "#FFF0C9", "#B78320"),
    "dados": ("Dados adicionais necessários",
              "painel pré/pós · unidades comparáveis · outcome externo",
              "#EEE9FF", "#7663A8"),
}


def desenhar_dag() -> None:
    fig, ax = plt.subplots(figsize=(16, 9), dpi=200)
    fig.patch.set_facecolor("#F7F8FA")
    ax.set_facecolor("#F7F8FA")
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis("off")

    def arrow(a, b, color="#586273", curve=0.0, dashed=False):
        ax.add_patch(FancyArrowPatch(
            POS[a], POS[b],
            arrowstyle="-|>", mutation_scale=16, linewidth=2.0,
            color=color, linestyle="dashed" if dashed else "solid",
            connectionstyle=f"arc3,rad={curve}",
            shrinkA=78, shrinkB=78, zorder=1,
        ))

    arrow("cad",   "gdp",   color="#3977A8")
    arrow("cad",   "out",   color="#3977A8", curve=-0.18)
    arrow("gdp",   "out",   color="#378253")
    arrow("gdp",   "mech",  color="#B78320")
    arrow("mech",  "out",   color="#B78320", curve=-0.12)
    arrow("dados", "gdp",   color="#7663A8", dashed=True)
    arrow("dados", "out",   color="#7663A8", curve=-0.15, dashed=True)

    for key, (title, subtitle, fill, edge) in SPECS.items():
        x, y = POS[key]
        w = 4.0 if key != "dados" else 4.3
        ax.add_patch(FancyBboxPatch(
            (x - w / 2, y - 0.56), w, 1.12,
            boxstyle="round,pad=0.06,rounding_size=0.13",
            facecolor=fill, edgecolor=edge, linewidth=1.7, zorder=3,
        ))
        ax.text(x, y + 0.16, title, ha="center", va="center",
                fontsize=11, fontweight="bold", color="#172033", zorder=4)
        ax.text(x, y - 0.21, subtitle, ha="center", va="center",
                fontsize=8.4, color="#4B5563", zorder=4)

    ax.text(0.5, 8.55,
            "DAG proposto para uma futura avaliação de impacto do Gás do Povo",
            fontsize=20, fontweight="bold", color="#172033")
    ax.text(0.5, 8.12,
            "O resultado deve ser externo ao pagamento do voucher e mensurado antes e após o programa",
            fontsize=11.5, color="#536074")

    note = (
        "ANÁLISE DISPONÍVEL AGORA  •  As bases atuais (Portal da Transparência e dados.gov.br) "
        "permitem estudar fatores associados à cobertura e ao valor do benefício.\n"
        "Elas não contêm resultado social externo nem contrafactual, portanto não identificam "
        "impacto causal. Para avaliação de impacto, é necessário um painel município-ano\n"
        "com desfecho externo (ex.: segurança alimentar, saúde) e um desenho "
        "quasi-experimental (DiD, PSM, RDD)."
    )
    ax.text(0.5, 1.6, note, fontsize=9.8, color="#7A4D11", ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.6", facecolor="#FFF7E3",
                      edgecolor="#D7A94E", linewidth=1.3))

    legend_items = [
        mpatches.Patch(facecolor="#DCEBFA", edgecolor="#3977A8",
                       label="Características prévias (confundidores)"),
        mpatches.Patch(facecolor="#DDF3E4", edgecolor="#378253",
                       label="Tratamento (Gás do Povo)"),
        mpatches.Patch(facecolor="#FADDDD", edgecolor="#B84D4D",
                       label="Resultado social externo"),
        mpatches.Patch(facecolor="#FFF0C9", edgecolor="#B78320",
                       label="Mecanismos pós-programa"),
        mpatches.Patch(facecolor="#EEE9FF", edgecolor="#7663A8",
                       label="Dados adicionais necessários"),
    ]
    ax.legend(handles=legend_items, loc="lower right", fontsize=9,
              framealpha=0.85, edgecolor="#CCCCCC",
              bbox_to_anchor=(0.99, 0.01))

    plt.savefig(DAG_PATH, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"DAG salvo em: {DAG_PATH}")


if __name__ == "__main__":
    desenhar_dag()
