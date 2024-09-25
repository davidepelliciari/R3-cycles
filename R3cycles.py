## R3 cycles viewer
## by Davide Pelliciari (INAF-IRA, Bologna, Italy) (25-Sept-2024)

import numpy as np
from astropy.time import Time
import datetime
import os
import argparse

def date_to_MJD(Times):
    t = Time(Times, format='isot')
    return t.mjd

def MJD_to_date(Times):
    t = Time(Times, format='mjd')
    return t.isot

def JD_to_MJD(JD_time):
    return JD_time - 2400000.5

def MJD_to_JD(MJD_time):
    return MJD_time + 2400000.5

def dt_DM(f1, DM):
    dtDM = 4.15 * 1.e+3 * (f1**-2) * DM
    dtDM = (dtDM / 3600.) / 24.
    return dtDM

def get_ToA(MJDstart, tsec, DM):
    tsec = tsec / 3600. / 24.
    return MJDstart + tsec - np.abs(dt_DM(415.854456, DM))

phi_0 = 58369.40  # MJD of 1st cycle (CHIME/FRB)
P = 16.33         # reported period (Pleunis+21)
DeltaT = 5.2      # window duration around peak

phi_0 += P / 2.

def get_cycle_range(Ncycle, start_from=phi_0):
    for ii in range(Ncycle):
        phi = start_from + ii * P
        phi_start = phi - DeltaT / 2.
        phi_end = phi + DeltaT / 2.
        yield (ii+1, MJD_to_date(phi_start), MJD_to_date(phi), MJD_to_date(phi_end))

def find_nearest_cycle():
    today = datetime.datetime.now()
    today_mjd = date_to_MJD(today.isoformat())
    n = round((today_mjd - phi_0) / P)
    nearest_phi = phi_0 + n * P
    nearest_start = nearest_phi - DeltaT / 2.
    nearest_end = nearest_phi + DeltaT / 2.
    return 1, MJD_to_date(nearest_start), MJD_to_date(nearest_phi), MJD_to_date(nearest_end)

def cycles_in_month(year, month):
    first_of_month = datetime.datetime(year, month, 1)
    next_month = (first_of_month.replace(day=28) + datetime.timedelta(days=4)).replace(day=1)
    first_of_month_mjd = date_to_MJD(first_of_month.isoformat())
    next_month_mjd = date_to_MJD(next_month.isoformat())
    
    cycles = []
    n = 0
    while True:
        phi = phi_0 + n * P
        if phi > next_month_mjd:
            break
        if phi >= first_of_month_mjd:
            phi_start = phi - DeltaT / 2.
            phi_end = phi + DeltaT / 2.
            cycles.append((n+1, MJD_to_date(phi_start), MJD_to_date(phi), MJD_to_date(phi_end)))
        n += 1
    return cycles

def log_cycles(log, cycles):
    if log:
        # Determine the script's directory and create 'S1cycles' folder
        script_dir = os.path.dirname(os.path.abspath(__file__))
        log_dir = os.path.join(script_dir, "S1cycles")
        os.makedirs(log_dir, exist_ok=True)
        
        # Create a unique filename for the log
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"S1_{timestamp}.dat"
        log_path = os.path.join(log_dir, log_file)
        
        # Write cycles to the log file
        with open(log_path, 'w') as f:
            f.write("Cycle_Number Start_Date Peak_Date End_Date\n")
            for cycle in cycles:
                f.write(f"{cycle[0]} {cycle[1]} {cycle[2]} {cycle[3]}\n")
        print(f"Log saved to: {log_path}")

def display_cycles(log=False):
    while True:
        print("\nChoose an option:")
        print("1: Find the nearest cycle to today's date")
        print("2: Display cycles for a given month and year")
        print("3: Display all cycles from the first")
        print("4: Display N cycles starting from the nearest cycle")
        print("0: Exit")
        
        choice = input("\nEnter your choice: ")
        
        if choice == '1':
            cycle = [find_nearest_cycle()]
            for (cycle_number, start, peak, end) in cycle:
                print(f"CYCLE {cycle_number}\nStart: {start}\nPeak: {peak}\nEnd: {end}\n")
            log_cycles(log, cycle)
        
        elif choice == '2':
            year = int(input("Enter year (YYYY): "))
            month = int(input("Enter month (MM): "))
            cycles = cycles_in_month(year, month)
            if cycles:
                for i, (cycle_number, start, peak, end) in enumerate(cycles):
                    print(f"CYCLE {cycle_number}\nStart: {start}\nPeak: {peak}\nEnd: {end}\n")
            else:
                print("No cycles found for this month.")
            log_cycles(log, cycles)
        
        elif choice == '3':
            Ncycle = int(input("How many cycles you want to display? "))
            cycles = list(get_cycle_range(Ncycle))
            for (cycle_number, start, peak, end) in cycles:
                print(f"CYCLE {cycle_number}\nStart: {start}\nPeak: {peak}\nEnd: {end}\n")
            log_cycles(log, cycles)
        
        elif choice == '4':
            Ncycle = int(input("How many cycles you want to display? "))
            nearest_start, nearest_peak, nearest_end = find_nearest_cycle()
            nearest_mjd = date_to_MJD(nearest_peak)
            cycles = list(get_cycle_range(Ncycle, start_from=nearest_mjd))
            for (cycle_number, start, peak, end) in cycles:
                print(f"CYCLE {cycle_number}\nStart: {start}\nPeak: {peak}\nEnd: {end}\n")
            log_cycles(log, cycles)
        
        elif choice == '0':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Cycle Display Program")
    parser.add_argument('--log', type=bool, default=False, help='Set to True to log output to a file.')
    args = parser.parse_args()
    
    display_cycles(log=args.log)
