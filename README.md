# R3 Cycles Viewer

This script allows you to view the activity windows of repeating FRB 20180916B, which shows periodic activity cycles ([https://ui.adsabs.harvard.edu/abs/2020Natur.582..351C/abstract](url)) and provides various options to filter the cycles. You can display the cycle closest to the current date, cycles within a specific month, all cycles from the beginning, or a predefined number of cycles starting from the nearest future cycle. The script also supports logging to a text file.

## Requirements

Before running the script, make sure you have the following libraries installed:

- `numpy`
- `astropy`
- `argparse`

You can install them with the following command:

```bash
pip install numpy astropy argparse
```

## Usage
### Available Options

The script offers several options to view the cycles. After running the script, the user can choose from the following options:

1. Find the nearest cycle to today's date: Displays the closest active cycle to the current date;
2. Display cycles for a specific month and year: Requests a specific year and month, and displays all cycles occurring within that period;
3. Display all cycles from the start: Shows all cycles starting from the first up to a user-specified number;
4. Display N cycles starting from the nearest future cycle: Starts from the cycle closest to the current date and displays a user-specified number of future cycles;

### Running the Script

You can run the script with:

```python
python script.py [--log True/False]
```

### Parameters:

```--log```: (Optional) Set to ```True``` if you want to save the output to a log file. If not specified, the default value is ```False```.

### Example:

```python
python R3cycles.py --log True
```

If ```--log``` is set to ```True```, the script will generate a log file in the S1cycles directory, which is located in the same folder as the script. The log file will contain a table with the following columns:

The file will contain a table with 4 columns:

```Cycle_Number  Start_Date  Peak_Date  End_Date```

Each row represents a cycle, with its corresponding start, peak, and end dates.

Log files will be named in the format ```S1_YYYYMMDD_HHMMSS.dat```, where ```YYYYMMDD_HHMMSS``` represents the date and time when the log was created.
