# seismic-ml
Machine Learning using Raspberry Shake.


## Data Renaming Script (Optional)

This script renames data files downloaded from Raspberry Shake to a more readable format.

### Input Format

The downloaded files will have names like:

```
AM.R716E.00.EHZ.D.2024.089
AM.R716E.00.EHZ.D.2024.090
AM.R716E.00.EHZ.D.2024.091
...
```

### Output Format

The script renames the files to the following format:

```
2024-03-29.mseed
2024-03-30.mseed
2024-03-31.mseed
...
```

### Usage

1. Create a folder called `raw-data` in the same directory as the script.
2. Divide the downloaded data into weekly chunks and place them in subfolders using the following naming convention:
   - `raw-data/week-1`
   - `raw-data/week-2`
   - `raw-data/week-3`
   - `raw-data/week-4`
   - `raw-data/week-5`
3. Run the Jupyter Notebook `data_renaming.ipynb`.

### Output

After running the script, the renamed files will be saved in folders called:

- `fixed-data/week-1`
- `fixed-data/week-2`
- `fixed-data/week-3`
- `fixed-data/week-4`
- `fixed-data/week-5`

The script will create the output folder automatically if it doesn't already exist.

---
