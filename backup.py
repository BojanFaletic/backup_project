#!/bin/python3
import os
import datetime


class Backup:
    time_format = "%m-%d-%Y_%H:%M"

    def __init__(self, folder_to_backup):
        if not os.path.isdir(folder_to_backup+'_backup'):
            os.makedirs(folder_to_backup+'_backup')
        self.backup_folder = folder_to_backup

    # remove all folders with _backup
    def remove_backup(self):
        folders = os.listdir('.')
        for folder in folders:
            if '_backup' in folder:
                os.removedirs(folder)

    # make backup
    def backup(self):
        current_time = datetime.datetime.now().strftime(self.time_format)
        os.system(
            f"zip -9 {self.backup_folder}_backup/{current_time}.zip {self.backup_folder}")

    # count elements below number threshold in sorted list
    def dates_elements(self, list_of_el, min_number, max_number, time_table):
        dates = []
        for el, tab in zip(list_of_el, time_table):
            if min_number <= el < max_number:
                dates.append(tab)
            if el >= max_number:
                break
        return dates

    # determine how many files can exist by interval
    def get_interval_seconds(self, n=6, total_size=80):
        start = 15
        elements = [int(start*60*(2**(x/n))) for x in range(total_size)]
        return elements

    def remove_single_backup(self, backup_name):
        c_dir = os.getcwd()
        os.remove(c_dir + '/' + self.backup_folder + '_backup/' + backup_name)

    # get distance from now to file
    def handle_backup(self):
        files = os.listdir(self.backup_folder+'_backup')

        # find all distances in time
        diff = []
        for file in files:
            time = file.split('.zip')[0]
            t = datetime.datetime.strptime(time, self.time_format)
            now = datetime.datetime.now()
            diff.append(round((now - t).total_seconds()))
        diff.sort()

        # get interval time
        required_times = [0] + self.get_interval_seconds()
        required_interval = [
            [required_times[i-1], required_times[i]] for i in range(1, len(required_times))]

        # if needed add newest backup
        if len(self.dates_elements(diff, required_interval[0][0], required_interval[0][1], diff)) == 0:
            self.backup()

        # clean older redundant backup
        for interval in required_interval:
            dates = self.dates_elements(diff, interval[0], interval[1], files)
            # too many backups in given interval, remove oldest
            while len(dates) > 1:
                print("Removing oldest dates from :", dates)
                self.remove_single_backup(dates[0])
                dates = dates[1:]


if __name__ == "__main__":
    b = Backup('backup_pos')
    b.handle_backup()
