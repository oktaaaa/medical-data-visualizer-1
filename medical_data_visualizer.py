import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv('medical_examination.csv')

# Add 'overweight' column
cm_m = (df['height']/100)**2
bmi = df['weight']/ cm_m

df['overweight'] = bmi.apply(lambda x:1 if x>25 else 0 )

# Normalize data by making 0 always good and 1 always bad. If the value of 'cholestorol' or 'gluc' is 1, make the value 0. If the value is more than 1, make the value 1.

# cholesterol normalization
df['gluc'] = df['gluc'].apply(lambda x: 1 if x>1 else 0)

# gluc normalization
df['cholesterol'] = df['cholesterol'].apply(lambda x: 1 if x>1 else 0)


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat =  pd.melt(df, id_vars = ['cardio'], value_vars = ['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])


    # Set up the matplotlib figure and draw the catplot
    figz = sns.catplot(data=df_cat, 
                        kind='count', 
                        x='variable', 
                        hue='value', 
                        col='cardio')
    figz.set_axis_labels('variable', 'total')
    fig = figz.fig
    
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[
      (df['ap_lo'] <= df['ap_hi'])
      & (df['height'] >= df['height'].quantile(0.025))
      & (df['height'] <= df['height'].quantile(0.975))
      & (df['weight'] >= df['weight'].quantile(0.025))
      & (df['weight'] <= df['weight'].quantile(0.975))
      ]

    # Generate a mask for the upper triangle
    corr = df_heat.corr()
    mask = np.triu(corr)
    fig, ax = plt.subplots(figsize = (11,9))
    cmap = sns.diverging_palette(230, 20, as_cmap=True)
    ax =sns.heatmap(corr,
                    mask=mask, 
                    cmap=cmap, 
                    fmt = '.1f',
                    square=True, 
                    linewidths=1, 
                    annot = True,
                    cbar_kws={"shrink": .5})

    fig.savefig('heatmap.png')
    return fig
