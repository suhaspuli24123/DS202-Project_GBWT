# import pandas as pd
# import matplotlib.pyplot as plt
# import seaborn as sns
# import numpy as np

# # Set the style for the plots
# sns.set_style('whitegrid')
# plt.rcParams.update({'font.size': 12})

# df = pd.read_csv('performance_metrics.csv')

# # Create individual plots with consistent styling
# def create_plot(metric, color, title, ylabel, figsize=(10, 6)):
#     plt.figure(figsize=figsize)
#     ax = sns.barplot(x='Step', y=metric, data=df, color=color)
    
#     # Add value labels on top of bars
#     for i, p in enumerate(ax.patches):
#         height = p.get_height()
#         ax.text(p.get_x() + p.get_width()/2.,
#                 height + 5,
#                 f'{height:.0f}',
#                 ha="center", fontsize=11)
    
#     # Set title and labels
#     plt.title(title, fontsize=14, pad=20)
#     plt.ylabel(ylabel, fontsize=12)
#     plt.xlabel('', fontsize=12)  # Empty x-label as in the original
    
#     # Adjust y-axis to match the style in the images
#     y_max = max(df[metric]) * 1.15  # Add 15% padding
#     plt.ylim(0, y_max)
    
#     # Tight layout
#     plt.tight_layout()
    
#     return plt

# # 1. Memory Usage Plot (Orange)
# memory_plot = create_plot(
#     'Memory_MB', 
#     'orange', 
#     'chr22: Memory Usage for VG / XG / GBWT',
#     'Memory Usage (MB)'
# )
# memory_plot.savefig('chr22_memory_usage.png', dpi=300)
# memory_plot.close()

# # 2. Runtime Plot (Light Blue)
# runtime_plot = create_plot(
#     'Runtime_Seconds', 
#     'skyblue', 
#     'chr22: Runtime for VG / XG / GBWT',
#     'Runtime (seconds)'
# )
# runtime_plot.savefig('chr22_runtime.png', dpi=300)
# runtime_plot.close()

# # 3. File Size Plot (Green)
# filesize_plot = create_plot(
#     'FileSize_MB', 
#     'green', 
#     'chr22: Output File Sizes for VG / XG / GBWT',
#     'File Size (MB)'
# )
# filesize_plot.savefig('chr22_filesize.png', dpi=300)
# filesize_plot.close()

# # Create a combined figure with all three plots
# fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# # Memory Usage
# sns.barplot(x='Step', y='Memory_MB', data=df, color='orange', ax=axes[0])
# axes[0].set_title('chr22: Memory Usage for VG / XG / GBWT', fontsize=14)
# axes[0].set_ylabel('Memory Usage (MB)')
# axes[0].set_ylim(0, max(df['Memory_MB']) * 1.15)

# # Runtime
# sns.barplot(x='Step', y='Runtime_Seconds', data=df, color='skyblue', ax=axes[1])
# axes[1].set_title('chr22: Runtime for VG / XG / GBWT', fontsize=14)
# axes[1].set_ylabel('Runtime (seconds)')
# axes[1].set_ylim(0, max(df['Runtime_Seconds']) * 1.15)

# # File Size
# sns.barplot(x='Step', y='FileSize_MB', data=df, color='green', ax=axes[2])
# axes[2].set_title('chr22: Output File Sizes for VG / XG / GBWT', fontsize=14)
# axes[2].set_ylabel('File Size (MB)')
# axes[2].set_ylim(0, max(df['FileSize_MB']) * 1.15)

# # Add value labels to all bars in the combined plot
# for i, ax in enumerate(axes):
#     metric = ['Memory_MB', 'Runtime_Seconds', 'FileSize_MB'][i]
#     for j, p in enumerate(ax.patches):
#         height = p.get_height()
#         ax.text(p.get_x() + p.get_width()/2.,
#                 height + 5,
#                 f'{height:.0f}',
#                 ha="center")

# plt.tight_layout()
# plt.savefig('chr22_combined_metrics.png', dpi=300)
# plt.close()

# print("All plots have been generated successfully!")



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