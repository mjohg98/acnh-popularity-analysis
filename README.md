## Animal Crossing New Horizons: Popularity Analysis

This repository contains code for the analysis of the popularity of villagers from the video game Animal Crossing New Horizons. The primary motivation was to understand if popularity was related to certain charactersitics such as species, gender, personality or hobby.

The working dataset was created by merging two datasets: a villager dataset found on Kaggle and a popularity dataset which was derived via poll data complied monthly from August 2020 to July 2022 at https://www.animalcrossingportal.com/tier-lists/new-horizons/all-villagers. 

  * Villager data is contained in "villager.csv" and the poll data in the zip file "acnh popularity data". 

Analysis was carried out entirely using standard Python libraries for data analysis including NumPy, Pandas, SciPy and matplotlib for the visualisations. The Python file "test" contains functions used to compute key statistics and create visuals. Code, methodology and analysis is written in the Jupyter notebook named "acnh_workbook".  

Credits: 

* [Villager data](https://www.kaggle.com/datasets/jessicali9530/animal-crossing-new-horizons-nookplaza-dataset)

* [Template for violin plots](https://www.python-graph-gallery.com/web-ggbetweenstats-with-matplotlib)
