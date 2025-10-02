import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

def draw_court():
    """Generate NBA court lines as Plotly shapes."""
    shapes = []
    
    # Court outline
    shapes.append(dict(
        type="rect",
        x0=-250, y0=-47.5, x1=250, y1=422.5,
        line=dict(color="#2c3e50", width=3),
        fillcolor="rgba(0,0,0,0)"
    ))
    
    # Hoop
    shapes.append(dict(
        type="circle",
        x0=-7.5, y0=-7.5, x1=7.5, y1=7.5,
        line=dict(color="#2c3e50", width=2),
        fillcolor="rgba(0,0,0,0)"
    ))
    
    # Backboard
    shapes.append(dict(
        type="line",
        x0=-30, y0=-12.5, x1=30, y1=-12.5,
        line=dict(color="#2c3e50", width=3)
    ))
    
    # Paint (outer box)
    shapes.append(dict(
        type="rect",
        x0=-80, y0=-47.5, x1=80, y1=142.5,
        line=dict(color="#2c3e50", width=2),
        fillcolor="rgba(0,0,0,0)"
    ))
    
    # Paint (inner box)
    shapes.append(dict(
        type="rect",
        x0=-60, y0=-47.5, x1=60, y1=142.5,
        line=dict(color="#2c3e50", width=2),
        fillcolor="rgba(0,0,0,0)"
    ))
    
    # Free throw circle (top arc)
    theta = np.linspace(0, np.pi, 50)
    x_ft = 60 * np.cos(theta)
    y_ft = 60 * np.sin(theta) + 142.5
    shapes.append(dict(
        type="path",
        path=f"M {x_ft[0]},{y_ft[0]} " + " ".join([f"L {x},{y}" for x, y in zip(x_ft[1:], y_ft[1:])]),
        line=dict(color="#2c3e50", width=2)
    ))
    
    # Free throw circle (bottom arc - dashed)
    shapes.append(dict(
        type="path",
        path=f"M {-x_ft[0]},{y_ft[0]} " + " ".join([f"L {-x},{y}" for x, y in zip(x_ft[1:], y_ft[1:])]),
        line=dict(color="#2c3e50", width=2, dash="dash")
    ))
    
    # Restricted area
    theta_rest = np.linspace(0, np.pi, 50)
    x_rest = 40 * np.cos(theta_rest)
    y_rest = 40 * np.sin(theta_rest)
    shapes.append(dict(
        type="path",
        path=f"M {x_rest[0]},{y_rest[0]} " + " ".join([f"L {x},{y}" for x, y in zip(x_rest[1:], y_rest[1:])]),
        line=dict(color="#2c3e50", width=2)
    ))
    
    # Three-point line (arc)
    theta_3pt = np.linspace(0.395, np.pi - 0.395, 100)
    x_3pt = 237.5 * np.cos(theta_3pt)
    y_3pt = 237.5 * np.sin(theta_3pt)
    shapes.append(dict(
        type="path",
        path=f"M {x_3pt[0]},{y_3pt[0]} " + " ".join([f"L {x},{y}" for x, y in zip(x_3pt[1:], y_3pt[1:])]),
        line=dict(color="#2c3e50", width=2)
    ))
    
    # Three-point line (corners)
    shapes.append(dict(
        type="line",
        x0=-220, y0=-47.5, x1=-220, y1=92.5,
        line=dict(color="#2c3e50", width=2)
    ))
    shapes.append(dict(
        type="line",
        x0=220, y0=-47.5, x1=220, y1=92.5,
        line=dict(color="#2c3e50", width=2)
    ))
    
    # Center court
    shapes.append(dict(
        type="circle",
        x0=-60, y0=362.5, x1=60, y1=482.5,
        line=dict(color="#2c3e50", width=2),
        fillcolor="rgba(0,0,0,0)"
    ))
    
    return shapes

def draw_plot(player_shotchart_df, title, div_id='shot-chart', include_plotlyjs='cdn'):
    """Generate interactive shot chart using Plotly and return as HTML div.
    
    Args:
        player_shotchart_df: DataFrame containing shot data
        title: Chart title
        div_id: Unique div ID for the chart (default: 'shot-chart')
        include_plotlyjs: How to include Plotly JS ('cdn', True, False) - use 'cdn' for first chart, False for subsequent
    """
    
    # Separate made and missed shots
    missed = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Missed Shot']
    made = player_shotchart_df[player_shotchart_df['EVENT_TYPE'] == 'Made Shot']
    
    # Calculate stats
    total_shots = len(player_shotchart_df)
    made_shots = len(made)
    fg_pct = (made_shots / total_shots * 100) if total_shots > 0 else 0
    
    # Create figure
    fig = go.Figure()
    
    # Add missed shots
    fig.add_trace(go.Scatter(
        x=missed['LOC_X'],
        y=missed['LOC_Y'],
        mode='markers',
        name='Missed',
        marker=dict(
            symbol='x',
            size=8,
            color='#e74c3c',
            line=dict(width=2, color='#e74c3c'),
            opacity=0.6
        ),
        hovertemplate='<b>Missed Shot</b><br>' +
                      'Distance: %{customdata[0]} ft<br>' +
                      'Shot Type: %{customdata[1]}<br>' +
                      '<extra></extra>',
        customdata=np.column_stack((
            missed['SHOT_DISTANCE'].values,
            missed['ACTION_TYPE'].values
        ))
    ))
    
    # Add made shots
    fig.add_trace(go.Scatter(
        x=made['LOC_X'],
        y=made['LOC_Y'],
        mode='markers',
        name='Made',
        marker=dict(
            symbol='circle',
            size=8,
            color='rgba(39, 174, 96, 0)',
            line=dict(width=2.5, color='#27ae60'),
            opacity=0.8
        ),
        hovertemplate='<b>Made Shot</b><br>' +
                      'Distance: %{customdata[0]} ft<br>' +
                      'Shot Type: %{customdata[1]}<br>' +
                      '<extra></extra>',
        customdata=np.column_stack((
            made['SHOT_DISTANCE'].values,
            made['ACTION_TYPE'].values
        ))
    ))
    
    # Update layout
    fig.update_layout(
        title=dict(
            text=f"{title}<br><sub>FG%: {fg_pct:.1f}% ({made_shots}/{total_shots})</sub>",
            font=dict(size=22, color='#1a1a1a', family='Arial, sans-serif'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            range=[-250, 250],
            showgrid=False,
            showticklabels=False,
            zeroline=False,
        ),
        yaxis=dict(
            range=[-47.5, 422.5],
            showgrid=False,
            showticklabels=False,
            zeroline=False,
            scaleanchor="x",
            scaleratio=1
        ),
        shapes=draw_court(),
        plot_bgcolor='#f5f5f5',
        paper_bgcolor='white',
        height=700,
        width=650,
        showlegend=True,
        legend=dict(
            x=0.85,
            y=0.98,
            bgcolor='rgba(255,255,255,0.9)',
            bordercolor='#2c3e50',
            borderwidth=2,
            font=dict(size=12)
        ),
        hovermode='closest',
        margin=dict(l=20, r=20, t=80, b=20)
    )
    
    # Return as HTML div
    return fig.to_html(
        include_plotlyjs=include_plotlyjs,
        div_id=div_id,
        config={
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select2d', 'lasso2d'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': 'shot_chart',
                'height': 700,
                'width': 650,
                'scale': 2
            }
        }
    )