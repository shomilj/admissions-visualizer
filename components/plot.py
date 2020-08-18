import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def group_and_inject_rates(filtered, filtered_all, path):
    filtered = filtered.groupby(path).sum().reset_index()
    applied = filtered_all[filtered_all['Segment'] == 'Applied'].groupby(path).sum().reset_index()
    admitted = filtered_all[filtered_all['Segment'] == 'Admitted'].groupby(path).sum().reset_index()
    committed = filtered_all[filtered_all['Segment'] == 'SIR\'ed'].groupby(path).sum().reset_index()
    
    filtered['Admit Rate'] = 100 * (admitted['Headcount'] / applied['Headcount'])
    filtered['Yield Rate'] = 100 * (committed['Headcount'] / admitted['Headcount'])

    filtered['Admit Rate'] = filtered['Admit Rate'].fillna(0)
    filtered['Yield Rate'] = filtered['Yield Rate'].fillna(0)

    filtered = filtered[filtered['Headcount'] > 0]

    if len(path) == 1:
        filtered['Ratio'] = filtered['Headcount'] / sum(filtered['Headcount'])
    else:
        split1, split2 = path[0], path[1]
        counts = {r.get(split2): r.get('Headcount') for _, r in filtered.groupby(split2).sum().reset_index().iterrows()}
        filtered['Ratio'] = filtered.apply(lambda row : row.get('Headcount') / counts[row.get(split2)], axis=1)

    return filtered

def plot_barchart(filtered, filtered_all, path, y_axis):
    df = group_and_inject_rates(filtered, filtered_all, path)
    
    if len(path) == 1:
        split1 = path[0]
        fig = px.bar(df, x=split1, y=y_axis)
    else:
        split1 = path[0]
        split2 = path[1]
        categories = sorted(set(df[split1]))

        data = []
        for split in sorted(set(df[split2])):
            values = {row.get(split1): row.get(y_axis) for _, row in df[df[split2] == split].iterrows()}
            row = []
            for category in categories:
                row.append(values.get(category, 0))
            data.append(go.Bar(name=split, x=categories, y=row, hoverlabel = dict(namelength = -1)))
            
        fig = go.Figure(data=data)
        fig.update_layout(barmode='group')
    
    fig.update_layout({'font_family': 'Avenir Next', 'font_color': 'black'})
    fig.update_layout(yaxis_title=y_axis)
    fig.update_layout({'plot_bgcolor': '#f9f9f9'})
    fig.update_layout(margin={'b': 10})
    return fig

def plot_treemap(filtered, filtered_all, path, color_col, color_scale): 
    title = ''
    filtered = group_and_inject_rates(filtered, filtered_all, path)

    path = [px.Constant('All Students in Current Filter')] + path

    fig = px.treemap(filtered, 
                    path=path, 
                    values='Headcount', 
                    color=color_col, 
                    hover_data={'Admit Rate': True, 'Yield Rate': True}, 
                    color_continuous_scale=color_scale)

    fig.update_layout({'font_family': 'Avenir Next', 'font_color': 'black'})
    fig.update_layout(margin={'b': 10})
    fig.update_layout(title={'text': title, 'x': 0.5, 'y': 0.97, 'xanchor': 'center', 'yanchor': 'top'})
    
    fig._data_objs[0].hovertemplate = '%{id}<br><br>' + \
                                      'Headcount: %{value}<br>' + \
                                      'Fraction of Total: %{percentRoot:.2f}<br>' + \
                                      'Fraction of Parent: %{percentParent:.2f}<br>' + \
                                      'Admit Rate: %{customdata[0]:.2f}%<br>' + \
                                      'Yield Rate: %{customdata[1]:.2f}%'

    return fig