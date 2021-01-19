"""
function for crontab that loads data into database
"""
import todata.models.toronto_data_update as data
# TODO fix module not found when file is run from terminal

def sql_load():
    data.update_toronto_power()
    data.update_toronto_temp()

    return True

if __name__ == '__main__':
    sql_load()
    print("SQL load complete")