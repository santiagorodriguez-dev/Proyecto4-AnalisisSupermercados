import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore

def Comparacion_de_Precios_entre_Supermercados(df):

    estadisticas_precios = df.groupby(['supermercado', 'categoria']).agg(
        precio_promedio=('precio', 'mean'),
        precio_max=('precio', 'max'),
        precio_min=('precio', 'min')
    ).reset_index()

    plt.figure(figsize=(12, 6))
    sns.barplot(x='categoria', y='precio_promedio', hue='supermercado', data=estadisticas_precios, palette="Set3")
    plt.title('Comparación de Precios entre Supermercados')
    plt.ylabel(f'Precio Promedio (€)')
    plt.xlabel('')
    plt.legend(title='Supermercados', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()
