# backup_project

Simple class used for performing backup of folder on disk.
Folder is stored as .zip. Over time new .zip is also added and old .zip are
removed.

``` python
    # determine how many files can exist by interval
    def get_interval_seconds(self, n=6, total_size=80):
        start = 15
        elements = [int(start*60*(2**(x/n))) for x in range(total_size)]
        return elements
```

![Alt text](images/saves.png)
