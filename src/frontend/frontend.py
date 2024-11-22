"""
Frontend va fournir l'ensemble des méthodes permettant l'affichage.
"""

import streamlit as st
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
import plotly.express as px


def generate_layout():
    """
    Configure et génère la mise en page principale de l'application Streamlit.

    Retourne:
    - tuple : Contient le menu sélectionné et les objets de colonne pour structurer le contenu dans des sections.
    """
    # Configurer la page pour un affichage en pleine largeur
    st.set_page_config(
        page_title="Mange ta main",
        page_icon="src/frontend/images/favicon.png",  # Chemin relatif vers l'icône
        layout="wide",
    )
    # Titre principal de l'application
    st.image("src/frontend/images/mangetamain.jpg")

    menu = st.selectbox(
        "", ["Généralité", "Clusterisation", "Ingrédients qui vont bien ensemble"]
    )

    # Zone principale de contenu
    st.header(menu)

    # Utilisation des colonnes pour diviser la zone centrale en plusieurs sections
    with st.container():
        if menu == "Clusterisation":
            col1, col2 = st.columns([1, 2])
        else:
            col1, col2 = st.columns(2)

    with st.container():
        col3, col4 = st.columns(2)

    with st.container():
        col5, col6 = st.columns(2)

    # Footer ou informations supplémentaires
    st.markdown("---")
    st.text("powered by Telecom Paris Master IA")

    return menu, col1, col2, col3, col4, col5, col6


### Travaux sur les ingrédients ###
def display_cluster_recipe(df_recipes_ingredients):
    """
    Affiche les clusters d'ingrédients en fonction des recettes sous forme de graphique interactif.

    Paramètres:
    - df_recipes_ingredients : DataFrame contenant les informations de clusterisation et les coordonnées PCA.

    Cette fonction génère un graphique de dispersion où chaque point représente un ingrédient, coloré selon le cluster.
    """
    fig = px.scatter(
        df_recipes_ingredients,
        x="pca_x",
        y="pca_y",
        color="cluster",
        hover_data=["recette"],
        title="Cluster des ingrédients en fonction des recettes",
    )
    fig.update_layout(height=650)
    st.plotly_chart(fig)


def display_kmeans_ingredient(df_recipes_ingredients):
    """
    Affiche les clusters d'ingrédients en fonction des recettes sous forme de graphique interactif.

    Paramètres:
    - df_recipes_ingredients : DataFrame contenant les informations de clusterisation et les coordonnées PCA.

    Cette fonction génère un graphique de dispersion où chaque point représente un ingrédient, coloré selon le cluster.
    """
    fig = px.scatter(
        df_recipes_ingredients,
        x="x",
        y="y",
        color="cluster",
        hover_data=["ingredient"],
        title="Cluster des ingrédients en fonction des recettes",
    )
    st.plotly_chart(fig)


def display_cloud_ingredient(co_occurrence_matrix, selected_ingredient):
    """
    Affiche un nuage de points des ingrédients en utilisant les données fournies.

    Args:
        co_occurrence_matrix (DataFrame): La matrice de co-occurrence des ingrédients.
        selected_ingredient (str): L'ingrédient sélectionné pour afficher les co-occurrences.

    Returns
    -------
    None
    """
    # Exclure les zéros
    co_occurrences = co_occurrence_matrix.loc[selected_ingredient]
    co_occurrences = co_occurrences[co_occurrences > 0]

    # Générer les coordonnées radiales
    angles = np.linspace(0, 2 * np.pi, len(co_occurrences), endpoint=False)
    radius = co_occurrences.values / co_occurrences.max() * 10  # Échelle du rayon
    x = radius * np.cos(angles)
    y = radius * np.sin(angles)

    # Créer le DataFrame pour le graphique
    plot_data = pd.DataFrame(
        {
            "ingredient": co_occurrences.index,
            "x": x,
            "y": y,
            "weight": co_occurrences.values,
        }
    )

    # Ajouter le point central
    plot_data = pd.concat(
        [
            pd.DataFrame(
                {"ingredient": [selected_ingredient], "x": [0], "y": [0], "weight": [0]}
            ),
            plot_data,
        ]
    )

    # Visualisation avec Plotly
    fig = px.scatter(
        plot_data,
        x="x",
        y="y",
        text="ingredient",
        size="weight",
        title=f"Nuage de points pour '{selected_ingredient}'",
        labels={"x": "Position X", "y": "Position Y"},
    )
    fig.update_traces(textposition="top center")

    # Affichage dans Streamlit
    st.plotly_chart(fig)
