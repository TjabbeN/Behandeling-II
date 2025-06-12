import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from apply_graph_styling import apply_graph_styling

# Read the CSV files
df1 = pd.read_csv("meting1.csv")
df2 = pd.read_csv("meting2.csv")

# Combine the dataframes
frames = [df1, df2]
df = pd.concat(frames)
df.reset_index(inplace=True, drop=True) 

print("Combined data:")
print(df)
print(f"\nTotal measurements: {len(df)}")

# Separate measurements based on 0.6mm threshold
below_threshold = df[df["Value"] < 0.6]
above_threshold = df[df["Value"] >= 0.6]

print(f"\n--- MEASUREMENTS BELOW 0.6mm ---")
print(f"Count: {len(below_threshold)}")
if len(below_threshold) > 0:
    print("Values:")
    for _, row in below_threshold.iterrows():
        print(f"  {row['Name']}: {row['Value']:.3f} mm")
    
    average_below = np.average(below_threshold["Value"])
    print(f"Average of measurements below 0.6mm: {average_below:.4f} mm")
else:
    print("No measurements below 0.6mm")

print(f"\n--- MEASUREMENTS AT OR ABOVE 0.6mm ---")
print(f"Count: {len(above_threshold)}")
if len(above_threshold) > 0:
    average_above = np.average(above_threshold["Value"])
    print(f"Average of measurements at or above 0.6mm: {average_above:.4f} mm")
    
    print(f"\nRange of values above 0.6mm:")
    print(f"  Minimum: {above_threshold['Value'].min():.3f} mm")
    print(f"  Maximum: {above_threshold['Value'].max():.3f} mm")
else:
    print("No measurements at or above 0.6mm")

# Overall statistics
overall_average = np.average(df["Value"])
print(f"\n--- OVERALL STATISTICS ---")
print(f"Overall average: {overall_average:.4f} mm")
print(f"Overall range: {df['Value'].min():.3f} mm to {df['Value'].max():.3f} mm")

# Create visualization with custom styling
fig, ax = plt.subplots(figsize=(12, 8))

# Plot all measurements
x = np.arange(len(df))
colors = ['#D20824' if val < 0.6 else '#006CA9' for val in df["Value"]]
scatter = ax.scatter(x, df["Value"], c=colors, alpha=0.7, s=50)

# Add horizontal line at 0.6mm threshold
ax.axhline(y=0.6, color='#221F20', linestyle='--', linewidth=2, label='0.6mm threshold')

# Add horizontal lines for averages
if len(below_threshold) > 0:
    ax.axhline(y=average_below, color='#D20824', linestyle='-', alpha=0.8, linewidth=2,
                label=f'Avg below 0.6mm: {average_below:.3f}mm')

if len(above_threshold) > 0:
    ax.axhline(y=average_above, color='#006CA9', linestyle='-', alpha=0.8, linewidth=2,
                label=f'Avg above 0.6mm: {average_above:.3f}mm')

ax.set_xlabel('Measurement Index')
ax.set_ylabel('Diameter (mm)')
ax.set_title('Diameter Measurements with 0.6mm Threshold Analysis')
ax.legend()

# Apply custom styling
apply_graph_styling(ax, grid_on_y=True)

plt.tight_layout()
# plt.show()

# Create a histogram to show distribution with custom styling
fig, ax = plt.subplots(figsize=(10, 6))

# Create histogram
n, bins, patches = ax.hist(df["Value"], bins=20, alpha=0.7, color='#006CA9', edgecolor='#221F20')

# Color bars based on threshold
for i, patch in enumerate(patches):
    if bins[i] < 0.6:
        patch.set_facecolor('#D20824')
    else:
        patch.set_facecolor('#006CA9')

ax.axvline(x=0.6, color='#221F20', linestyle='--', linewidth=2, label='0.6mm drempelwaarde')
ax.axvline(x=overall_average, color='#2E8B57', linestyle='-', linewidth=2, 
           label=f'Globaal gem.: {overall_average:.3f} mm')

if len(below_threshold) > 0:
    ax.axvline(x=average_below, color='#D20824', linestyle='-', linewidth=2, 
                label=f'Gem. onder 0,6 mm: {average_below:.3f} mm')

if len(above_threshold) > 0:
    ax.axvline(x=average_above, color='#006CA9', linestyle='-', linewidth=2, 
                label=f'Gem. boven 0, 6mm: {average_above:.3f} mm')

ax.set_xlabel('Diameter (mm)')
ax.set_ylabel('Frequentie')
ax.set_title('Distributie v.d. gemeten diameters')
ax.legend()

# Apply custom styling
apply_graph_styling(ax, grid_on_y=True)

plt.tight_layout()
plt.show()