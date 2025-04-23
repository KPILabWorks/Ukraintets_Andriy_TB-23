import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

files = {
    'No barrier':       'data/wout_barier.csv',
    'See-through bag':  'data/seethru_bag.csv',
    'Piece of paper':   'data/piece_of_paper.csv',
}

# Read CSVs
data = {}
for label, path in files.items():
    df = pd.read_csv(path)
    df = df.rename(columns=lambda c: c.strip())
    data[label] = df


time = data['No barrier']['Time (s)'].values
combined = pd.DataFrame({'Time (s)': time})

for label, df in data.items():
    # interpolate df - so each series sits on the same time axis
    combined[label] = np.interp(time, df['Time (s)'].values, df['Illuminance (lx)'].values)

# Math statistics
summary = []
for label in files:
    y = combined[label]
    mean_lx = y.mean()
    std_lx  = y.std(ddof=1)
    min_lx  = y.min()
    max_lx  = y.max()
    auc_lx  = np.trapezoid(y, combined['Time (s)'])
    # 'No barrier' values is a standard
    if label != 'No barrier':
        pct = (y / combined['No barrier']) * 100
        mean_pct = pct.mean()
    else:
        mean_pct = 100.0
    summary.append({
        'Barrier':                      label,
        'Mean (lx)':                    mean_lx,
        'Standard Deviation (lx)':      std_lx,
        'Min (lx)':                     min_lx,
        'Max (lx)':                     max_lx,
        'Area under the curve (lx·s)':  auc_lx,
        'Mean % Transmission':          mean_pct
    })

summary_df = pd.DataFrame(summary)


# Summary table
print(summary_df.to_string(index=False))


plt.figure()
for label in files:
    plt.plot(combined['Time (s)'], combined[label], label=label)
plt.xlabel('Time (s)')
plt.ylabel('Illuminance (lx)')
plt.title('Phone Illuminance under Different Barriers')
plt.legend()
plt.grid(True)
plt.tight_layout()

plt.show()
