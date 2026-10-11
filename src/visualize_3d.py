import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("data/raw/exoplanets_clean.csv", low_memory=False)

# Clean up for the plot
plot_df = df.dropna(subset=['radius_earth', 'mass_earth', 'distance_parsec']).copy()

# Remove extreme outliers so the plot doesn't break
plot_df = plot_df[plot_df['radius_earth'] < 20]
plot_df = plot_df[plot_df['mass_earth'] < 2000]
plot_df = plot_df[plot_df['distance_parsec'] < 1000]

# Create the 3D Scatter Plot
fig = px.scatter_3d(
    plot_df, 
    x='radius_earth', 
    y='mass_earth', 
    z='distance_parsec',
    color='discovery_method',
    hover_name='planet_name',
    title='3D Exoplanet Map: Radius vs Mass vs Distance',
    labels={
        'radius_earth': 'Radius (Earth radii)',
        'mass_earth': 'Mass (Earth masses)',
        'distance_parsec': 'Distance (Parsecs)',
        'discovery_method': 'Discovery Method'
    },
    opacity=0.7
)

# Make it look nice
fig.update_layout(
    scene=dict(
        xaxis_title='Radius (Earth)',
        yaxis_title='Mass (Earth)',
        zaxis_title='Distance (Parsecs)'
    ),
    margin=dict(l=0, r=0, b=0, t=40)
)

# Save it as an interactive HTML file
fig.write_html("outputs/charts/3d_exoplanet_map.html")
print("Done! 3D chart saved to outputs/charts/3d_exoplanet_map.html")