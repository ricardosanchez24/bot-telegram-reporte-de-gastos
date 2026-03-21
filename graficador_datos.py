import io
import os
import matplotlib.pyplot as plt 
import numpy as np


def graficador(datos):

    fig, ax = plt.subplots(figsize=(8, 4), subplot_kw=dict(aspect="equal"))

    montos = [abs(float(x.split()[0])) for x in datos]
    categorias = [x.split()[-1] for x in datos]

    def func(pct,data):
        montos = int(np.round(pct/100.*np.sum(data)))
        return f"{pct:.1f}%\n{montos}Bs"

    pieza, text, text_pieza = ax.pie(montos,autopct=lambda pct: func(pct,montos),textprops=dict(color='w'))

    ax.set_title("Reporte de Gastos")

    plt.legend(pieza,categorias,
            title="Gastos",
            loc="center left",
            bbox_to_anchor=(1,0,0.5,1))

    plt.setp(text_pieza,size=8,weight="bold")

    #plt.show()

    ram = io.BytesIO()

    plt.savefig(ram,format="png")

    ram.seek(0)

    return ram