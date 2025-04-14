import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv('performance_metrics.csv')

# Set the style for the plots
sns.set_style('whitegrid')
plt.rcParams.update({'font.size': 12})

# Function to create individual plots
def create_plot(metric, color, title, ylabel, data, figsize=(10, 6)):
    plt.figure(figsize=figsize)
    ax = sns.barplot(x='Step', y=metric, data=data, color=color)
    
    # Add value labels on top of bars
    for i, p in enumerate(ax.patches):
        height = p.get_height()
        ax.text(p.get_x() + p.get_width()/2., height + 0.1,
                f'{height:.1f}', ha="center", va="bottom")
    
    plt.title(title, fontsize=14, pad=20)
    plt.ylabel(ylabel, fontsize=12)
    plt.xlabel('', fontsize=12)  # Empty x-label as in the original
    
    # Adjust y-axis to match the style in the images
    y_max = max(data[metric]) * 1.15  # Add 15% padding
    plt.ylim(0, y_max)
    
    plt.tight_layout()
    return plt

# Create DataFrame for VG, XG, and GBWT-10
base_df = df[df['Step'].isin(['VG', 'XG', 'GBWT-10'])].copy()
base_df.loc[base_df['Step'] == 'GBWT-10', 'Step'] = 'GBWT'

# Create individual plots
metrics = {
    'Memory_MB': ('orange', 'chr22: Memory Usage for VG / XG / GBWT', 'Memory Usage (MB)'),
    'Runtime_Seconds': ('skyblue', 'chr22: Runtime for VG / XG / GBWT', 'Runtime (seconds)'),
    'FileSize_MB': ('green', 'chr22: Output File Sizes for VG / XG / GBWT', 'File Size (MB)')
}

for metric, (color, title, ylabel) in metrics.items():
    plot = create_plot(metric, color, title, ylabel, base_df)
    plot.savefig(f'chr22_{metric}.png', dpi=300)
    plot.close()

# Create GBWT comparison plots
gbwt_df = df[df['Step'].str.startswith('GBWT-')].copy()
gbwt_df['Paths'] = gbwt_df['Paths'].astype(int)

for metric, (color, title, ylabel) in metrics.items():
    plt.figure(figsize=(10, 6))
    ax = sns.barplot(x='Paths', y=metric, data=gbwt_df, color=color)
    
    for i, p in enumerate(ax.patches):
        height = p.get_height()
        ax.text(p.get_x() + p.get_width()/2., height + 0.1,
                f'{height:.1f}', ha="center", va="bottom")
    
    plt.title(f'chr22: {ylabel} for GBWT with Different Path Counts', fontsize=14, pad=20)
    plt.ylabel(ylabel, fontsize=12)
    plt.xlabel('Number of Paths', fontsize=12)
    
    y_max = max(gbwt_df[metric]) * 1.15
    plt.ylim(0, y_max)
    
    plt.tight_layout()
    plt.savefig(f'chr22_GBWT_paths_{metric}.png', dpi=300)
    plt.close()

print("All plots have been generated successfully!")