import pandas as pd # type: ignore
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore

def Comparacion_de_Precios_promedio_entre_Supermercados(df):

    estadisticas_precios = df.groupby(['supermercado', 'categoria']).agg(
        precio_promedio=('precio', 'mean'),
        precio_max=('precio', 'max'),
        precio_min=('precio', 'min')
    ).reset_index()

    plt.figure(figsize=(12, 6))
    sns.barplot(x='supermercado', y='precio_promedio', hue='categoria', data=estadisticas_precios, palette="Set3")
    plt.title('Comparación de Precios entre Supermercados')
    plt.ylabel(f'Precio Promedio (€)')
    plt.xlabel('')
    plt.legend(title='Categorias', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()

def Comparacion_de_Precios_min_max_Supermercados(df):

    estadisticas_precios = df.groupby(['supermercado', 'categoria']).agg(
        precio_promedio=('precio', 'mean'),
        precio_max=('precio', 'max'),
        precio_min=('precio', 'min')
    ).reset_index()

    plt.figure(figsize=(12, 6))

    sns.lineplot(x='supermercado', y='precio_max', hue='categoria', data=estadisticas_precios, marker='o', palette="Set3")

    sns.lineplot(x='supermercado', y='precio_min', hue='categoria', data=estadisticas_precios, marker='x', linestyle='--', palette="Set3")

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
    
    plt.figure(figsize=(14, 8))
    sns.lineplot(x='fecha_format', y='precio_promedio', hue='supermercado', data=df_grouped, marker='o', palette="Set3")

    plt.title(f'Análisis de la Evolución de Precios de la categoria: {filtro}')
    plt.ylabel('Precio Promedio (€)')
    plt.xlabel('')
    plt.legend(title='Supermercados', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.show()

def dispersion_precios_supermercados(df, filtro):

    df_grouped = df.groupby([pd.Grouper(key='fecha_format', freq='ME'), 'categoria','supermercado','desc_producto']).agg(
            precio_promedio=('precio', 'mean'),
            precio_max=('precio', 'max'),
            precio_min=('precio', 'min')
    ).reset_index()

    df_grouped = df_grouped[df_grouped['categoria'] == filtro]

    #df_grouped = df_grouped[df_grouped['supermercado'] == 'mercadona']
    
    plt.figure(figsize=(20, 8))

    sns.scatterplot(x='fecha_format', y='precio_max', hue='supermercado', marker='o', data=df_grouped, s=100, palette="Set3")

    sns.scatterplot(x='fecha_format', y='precio_min', hue='supermercado', marker='x', data=df_grouped, s=100, palette="Set3")

    plt.title(f'Dispersión de Precios Máximos y Mínimos por Mes para productos de la categoria: {filtro}')
    plt.ylabel('Precio (€)')
    plt.xlabel('Fecha')
    plt.legend(title='Supermercado', bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.show()

    
