import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore

def comparacion_de_precios_promedio_entre_supermercados(df):

    estadisticas_precios = df.groupby(['supermercado', 'categoria']).agg(
        precio_promedio=('precio', 'mean'),
        precio_max=('precio', 'max'),
        precio_min=('precio', 'min')
    ).reset_index()

    plt.figure(figsize=(13, 6))
    sns.barplot(x='supermercado', y='precio_promedio', hue='categoria', data=estadisticas_precios, palette="Set2")
    plt.title('Comparación de Precios entre Supermercados')
    plt.ylabel(f'Precio Promedio (€)')
    plt.xlabel('')
    plt.legend(title='Categorias', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()

def comparacion_de_precios_min_max_Supermercados(df):

    estadisticas_precios = df.groupby(['supermercado', 'categoria']).agg(
        precio_promedio=('precio', 'mean'),
        precio_max=('precio', 'max'),
        precio_min=('precio', 'min')
    ).reset_index()

    plt.figure(figsize=(13, 6))

    sns.lineplot(x='supermercado', y='precio_max', hue='categoria', data=estadisticas_precios, marker='o', palette="Set2")

    sns.lineplot(x='supermercado', y='precio_min', hue='categoria', data=estadisticas_precios, marker='x', linestyle='--', palette="Set2")

    plt.title('Precios Máximos y Mínimos (----) por Supermercado y Categoría')
    plt.ylabel('Precio (€)')
    plt.xlabel('')
    plt.legend(title='Categorias', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()

def historico_precios_supermercados(df, filtro):

    df_grouped = df.groupby([pd.Grouper(key='fecha_format', freq='ME'), 'categoria','supermercado','desc_producto']).agg(
        precio_promedio=('precio', 'mean')
    ).reset_index()

    df_grouped = df_grouped[df_grouped['categoria'] == filtro]
    
    plt.figure(figsize=(13, 6))
    sns.lineplot(x='fecha_format', y='precio_promedio', hue='supermercado', data=df_grouped, marker='o', palette="Set2")

    plt.title(f'Análisis de la Evolución de Precios de la categoria: {filtro}')
    plt.ylabel('Precio Promedio (€)')
    plt.xlabel('')
    plt.legend(title='Supermercados', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.show()

    
