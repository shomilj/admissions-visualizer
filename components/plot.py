import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def group(data, categories):
    """
    Groups data on a category or multiple categories.
    Takes a weighted average of Admit Rate and Yield Rate 
    (since the original dataset represents demographics using bucketing).
    Sums over the Headcount column.
    """
    filtered = data.copy()
    filtered['Admit Rate'] = filtered['Admit Rate'] * filtered['Headcount']
    filtered['Yield Rate'] = filtered['Yield Rate'] * filtered['Headcount']
    filtered = filtered[filtered['Headcount'] != 0]
    weighted_average = lambda x: round(sum(x) / sum(filtered.loc[x.index, "Headcount"]), 2)
    filtered = filtered.groupby(categories).agg({
        'Admit Rate': weighted_average,
        'Yield Rate': weighted_average,
        'Headcount': 'sum'
    }).reset_index()
    return filtered

def plot_treemap(data, path, color_col, color_scale): 
    title = ''
    data = data.copy()    
    filtered = group(data, path) 
    path = [px.Constant('All Students in Current Filter')] + path

    # Calculate Percentages.    
    total = data.groupby('Academic Yr').sum()['Headcount']
    calculate_percentage = lambda row : 100 * (row.get('Headcount') / total)
    filtered.loc[:, 'Percent'] = filtered.apply(calculate_percentage, axis=1)    
    
    # Convert Admit Rate into Percentages.
    filtered['Admit Rate'] = filtered['Admit Rate'].apply(lambda x : x / 100)
    
    if color_col == 'Headcount':        
        fig = px.treemap(filtered, 
                         path=path, 
                         values='Headcount', 
                         color=color_col, 
                         hover_data={'Admit Rate': True, 'Percent': True}, 
                         color_continuous_scale=color_scale)
        
    elif color_col == 'Admit Rate':
        fig = px.treemap(filtered, 
                         path=path, 
                         values='Headcount', 
                         color=color_col, 
                         color_continuous_scale=color_scale,
                         hover_data={'Admit Rate': True, 'Percent': True}, )
    
    fig.update_layout({'font_family': 'Avenir Next', 'font_color': 'black'})
    fig.update_layout(margin={'b': 10})
    fig.update_layout(title={'text': title, 'x': 0.5, 'y': 0.97, 'xanchor': 'center', 'yanchor': 'top'})
    
    fig._data_objs[0].hovertemplate = '%{id}<br><br>' + \
                                      'Headcount: %{value}<br>' + \
                                      'Fraction of Total: %{percentRoot:.2f}<br>' + \
                                      'Fraction of Parent: %{percentParent:.2f}<br>' + \
                                      'Admit Rate: %{customdata[0]:.2f}'

    return fig