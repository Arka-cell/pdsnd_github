"""
    Importing our required libraries.
"""

import pandas as pd
from colorama import init, Fore, Back, Style
import requests
import sys
import os
from PIL import Image
import matplotlib.pyplot as plt
from glob import glob
import psutil
from datetime import datetime
from pandas.plotting import register_matplotlib_converters


"""
    In the text below, we will define all our options
"""

register_matplotlib_converters(explicit=True)

pd.set_option('display.max_columns', None) #This will display all the columns in the pd.head()

init(convert=True)



"""
    Below, we will define our functions
"""

#This is the main() function
def main(x,z):
    while(z == True):
        while (x==str(1)):
            y = (input('\nChoose a city from which you want to have an outlook on its raw data.\nPress 1 to choose Chicago.\nPress 2 to choose New York.\nPress 3 to choose Washington, DC.\nEnter here: ')).title()
            if (y == str(1) or y == str(2) or y == str(3)):
                rows_sample = (pd.read_csv(str(raw_files[y]))).head()
                print(Fore.MAGENTA+'\n',rows_sample)
                del rows_sample
                z = False
                x = 0
                break
            else:
                print(Fore.RED+'Please, type a correct number for your choice of city.'+Fore.WHITE)
        if (x == str(2)):
            print('\nYou will not see a sample from raw data.\n')
            z = False
            break
        elif (x == 0):
            break
        else:
            print(Fore.RED+'\nPlease, type a correct number for whether you want to see the raw data or not.\n'+Fore.WHITE)
            x = input('\nPress 1 if Yes.\nPress 2 if no.\nEnter here: ')

#Source: https://stackoverflow.com/questions/938733/total-memory-used-by-python-process
#https://stackoverflow.com/questions/39100971/how-do-i-release-memory-used-by-a-pandas-dataframe
#For the sake of the review I'll be showing memory usage, as we will try to make it as efficient as possible
def memory_usage():
    process = psutil.Process(os.getpid())
    #I am using an octothorp in the print function below, if you want to see the memory usage at real time, you can just delete it.
    #print('Memory Usage is: '+str(process.memory_info()[0] / float(2 ** 20))+' Megabytes')
    memory_statistcs.append(int(process.memory_info()[0] / float(2 ** 20)))
    time_statistics.append(str(datetime.utcnow())[14:20].replace(':','m').replace('.','s'))

#Creating functions that will perform operations to be called upon
def popular_time(x,z,y):
    """
    x represents the key of the dictionarry raw_files, z represents the number of the subquestion, month,
    day or hour. y represents the hour format, it is applicable only
    if z == 3, in other words, applicable only when we want to see the hour
    """
    file_csv = pd.read_csv(str(raw_files[x]),parse_dates=['Start Time'])
    memory_usage()
    if (z == '1' and y == '0'):
        file_csv['Month'] = file_csv['Start Time'].dt.month
        common_time = file_csv['Month'].mode()[0]
        print(Fore.BLUE + '\nThe most common month is:',str(months_mapper[common_time]))
    elif (z == '2' and y == '0'):
        file_csv['Day'] = file_csv['Start Time'].dt.dayofweek
        common_time = file_csv['Day'].mode()[0]
        print(Fore.BLUE + '\nThe most common day is: ',str(days_mapper[common_time]))
    elif (z == '3'):
        if (y == '1'):
            file_csv['Hour'] = file_csv['Start Time'].dt.hour
            common_time = file_csv['Hour'].mode()[0]
            print(Fore.BLUE + '\nThe most common hour is: ',str(hour_mapper_12[common_time]))
        elif (y == '2'):
            file_csv['Hour'] = file_csv['Start Time'].dt.hour
            common_time = file_csv['Hour'].mode()[0]
            print(Fore.BLUE + '\nThe most common hour is: ',str(hour_mapper_24[common_time]))
    """
    We'll call the del function to collect garbage and release it.
    """
    del file_csv
    memory_usage()

def stations(x,y):
    #x is the city and y is the sub-question
    file_csv = pd.read_csv(str(raw_files[x]))
    memory_usage()
    if (y == '1'):
        most_common_start = file_csv['Start Station'].mode()[0]
        print(Fore.BLUE + '\nThe Most Common Start Station is',str(most_common_start))
    elif (y == '2'):
        most_common_end = file_csv['End Station'].mode()[0]
        print(Fore.BLUE + '\nThe Most Common End Station is',str(most_common_end))
    elif (y == '3'):
        file_csv['Start to Ending Station'] = file_csv['Start Station']+[' to ']+file_csv['End Station']
        most_common_trip = file_csv['Start to Ending Station'].mode()[0]
        print(Fore.BLUE + '\nThe Most Common Trip Is From', str(most_common_trip))
    del file_csv
    memory_usage()

def travel(x,y):
    file_csv = pd.read_csv(str(raw_files[x]),parse_dates=['Start Time','End Time'])
    memory_usage()
    file_csv['Travel Time'] = file_csv['End Time'] - file_csv['Start Time']
    if (y == '1'):
        tot_trv_time = str((file_csv['Travel Time']).sum())
        print(Fore.BLUE + '\nThe Total Travel Time is',str(tot_trv_time))
    elif (y == '2'):
        avg_trv_time = str((file_csv['Travel Time']).mean())[:15]
        print(Fore.BLUE + '\nThe Average Travel Time is',str(avg_trv_time))
    del file_csv
    memory_usage()

def user_info(x, y, z):
    file_csv = pd.read_csv(str(raw_files[x]))
    if (y == str(1)):
        count = file_csv.groupby(['User Type'])['User Type'].count()
        print(Fore.BLUE + '\nThe Total Number for Each Subscribers Type is: \n'+str(count))
    elif (y == str(2) and(x == str(1) or x == str(2))):
        count_gender = file_csv.groupby(['Gender'])['Gender'].count()
        print(Fore.BLUE + '\nThe Total Number for Each Gender is: \n'+str(count_gender))
    elif (y == str(3) and z == str(1)):
        earliest = int(file_csv['Birth Year'].min())
        print(Fore.BLUE + '\nThe earliest birth year is '+ str(earliest))
        print(Fore.YELLOW+'\nNote! \nAn earliest birthyear such as 1899 in Chicago might suggest that the data contains \nfalse values that need to be checked. The probability of someone born in that \nyear being able to drive a bike is near none-existant. ')
    elif (y == str(3) and z == str(2)):
        recent = int(file_csv['Birth Year'].max())
        print(Fore.BLUE + '\nThe most recent birth year is '+str(recent))
        print(Fore.YELLOW+'\nNote! \nA recent birthday like 2016 in Chicago, suggest that the data contains false values.')
    elif (y == str(3) and z == str(3)):
        common_birthyear = int(file_csv['Birth Year'].mode()[0]) #I turned the code into int for the sake of interactivity. The result type is in a float; showing for example '1989.0'.
        print(Fore.BLUE + '\nThe most common birth year is '+str(common_birthyear))
    del file_csv
    memory_usage()

"""
    Assigning our variables, lists, dictionaries
"""
memory_statistcs = [] 
time_statistics = [] 


working_dir = (os.path.realpath(__file__))[:(len((os.path.realpath(__file__))) - (len(os.path.basename(__file__))))]
csv_files_dir = (glob(working_dir+"\\*.csv"))
raw_files = {}
i = 1

for element in csv_files_dir:
    raw_files[str(i)] = element
    i = i + 1

#The start variable will initialize the script, if we have to quit, we just turn it into False. It is the same thing for download_is_starting
start = True
download_is_starting = True
months_mapper = {
                1:'January', 2:'February',3:'March',4:'April',5:'May',6:'June',
                7:'July',8:'August',9:'September',10:'October',11:'November',
                12:'December'
                }
days_mapper = {
                1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thursday',5:'Friday',
                6:'Saturday', 7:'Sunday'
                }
hour_mapper_12 = {
                0:'00:00 A.M', 1:'01:00 A.M',2:'02:00 A.M',3:'03:00 A.M',
                4:'04:00 A.M',5:'05:00 A.M',6:'06:00 A.M',7:'07:00 A.M',
                8:'08:00 A.M',9:'09:00 A.M',10:'10:00 A.M',11:'11:00 A.M',
                12:'00:00 P.M',13:'01:00 P.M',14:'02:00 P.M',15:'03:00 P.M',
                16:'04:00 P.M',17:'05:00 P.M',18:'06:00 P.M',19:'07:00 P.M',
                20:'08:00 P.M',21:'09:00 P.M',22:'10:00 P.M',23:'11:00 P.M'
                }
hour_mapper_24 = {
                0:'00:00', 1:'01:00',2:'02:00',3:'03:00',4:'04:00',5:'05:00',
                6:'06:00',7:'07:00',8:'08:00',9:'09:00',10:'10:00',11:'11:00',
                12:'12:00',13:'13:00',14:'14:00',15:'15:00',16:'16:00',17:'17:00',
                18:'18:00',19:'19:00',20.:'20:00',21:'21:00',22:'22:00',23:'23:00'
                }
cities = 'Chicago', 'New York City', 'Washington, D.C'

"""
    Initializing our script.
"""
print(Fore.GREEN + Style.BRIGHT +'\nHi! And welcome. This script will answer and give specific statistics that were asked in the US Bikeshare Project.\n')

while (download_is_starting == True):
    print(Fore.WHITE+'\nAs part of the project, an image file will be downloaded from \'https://www.imgur.com\'. Don\'t worry! It is totally secure, \nand optional. Moreover, you are not obliged to download it.\n')
    download = (input('\nDo you want to proceed?\n\nType 1 if yes.\nType 2 if no.\nPress Q to quit\nEnter here: ')).title()
    if (download == str(1)):
        try:
            file_url = 'https://i.imgur.com/XZTkBix.jpg'
            file_name = 'Project Guide as Image.jpg'
            with open(file_name, "wb") as f:
                print ("Downloading "+file_name+"... please, wait for download progress\n")
                response = requests.get(file_url, stream=True)
                total_length = response.headers.get('content-length')

                if total_length is None: # no content length header
                    f.write(response.content)
                else:
                    #dl stands for data length, but will add up to itself and len(data)
                    dl = 0
                    total_length = int(total_length)
                    for data in response.iter_content(chunk_size=4096):
                        dl += len(data)
                        f.write(data)
                        done = int(100 * dl / total_length)
                        sys.stdout.write("\r[%s%s]" % (str(done)[:5]+ '%', ' ' * (0-done)) )
                        sys.stdout.flush()
                if (round(done) == 100):
                    print('\n'+str(round(done))+'% - Download Succeded!\n')
                else:
                    print(' - Download Failed.')
            im = Image.open('Project Guide as Image.jpg')
            im.show()
            download = str(2)
            download_is_starting = False
        except:
            print(Fore.RED + '\nAn error did occur during download.\nPlease, copy the following link to get the file: \''+file_url+'\'')
            download = str(2)

    elif(download == str(2)):
        download_is_starting = False
    elif (download == 'Q'):
        download_is_starting = False
        start = False
    else:
        print(Fore.RED + '\nType a correct number, or letter, for your choice.')
        continue

while(start == True):
    print(Fore.WHITE + Style.BRIGHT+'\nDo you want to see a sample of the raw data?\n')
    main(input('\nPress 1 if Yes.\nPress 2 if no.\nEnter here: '), True)
    memory_usage()

    if(download ==str (2) or download == str(1)):
        start = True
        print(Fore.WHITE+'\nYou can find different analytical questions from this script. Have fun!\n')
   
        while (start == True):
            print(Fore.WHITE+'\n   Choose one of the following options:\n\nPress 1 to get the most popular travel times.\nPress 2 to get the most common stations and trips.\nPress 3 to get the total and the average time of trips.\nPress 4 to get the total of each user type, gender, and information about age.\nTo quit press Q.\n')
            answer = (input('Type your choice here: ')).title()

            while (answer == str(1)):
                print(Fore.WHITE + Style.BRIGHT+'\nDo you want to see a sample of the raw data?\n')
                main(input('\nPress 1 if Yes.\nPress 2 if no.\nEnter here: '), True)
                memory_usage()
                print(Fore.WHITE+'\nChoose which city would you want for your statistics.\nPress 1 to choose Chicago.\nPress 2 to choose New York.\nPress 3 to choose Washington, DC.\nPress B to go back.\n')
                city = (input('Type your choice here: ')).title()

                while (city > str(0) and city < str(4) and len(city) == 1):
                    print(Fore.WHITE+'\nPress 1 to get the most common month.\nPress 2 to get the most common day.\nPress 3 to get the most common hour.\nPress B to go back.\n')
                    sub_answer = (input('Type your choice here: ')).title()
                    if (sub_answer > str(0) and sub_answer < str(3)):
                        popular_time(city, sub_answer, '0')
                    while (sub_answer == str(3)):
                        print(Fore.WHITE+'\nPress 1 for the 12-Hour Format.\nPress 2 for the 24-Hour Format.\n')
                        hour_format = input('Type your choice here: ')
                        if (hour_format == str(1) or hour_format == str(2)):
                            popular_time(city, sub_answer, hour_format)
                            break
                        else:
                            print(Fore.RED + '\nType a correct number, or letter, for your choice.')
                    if (sub_answer == 'B'):
                        break
                    elif (sub_answer != 'B' and (sub_answer > str(3) or sub_answer < str(1))):
                        print(Fore.RED + '\nType a correct number, or letter, for your choice.')
                if (city == 'B'):
                    break
                elif (city != 'B' and (city < str(1) or city > str(3))):
                    print(Fore.RED + '\nType a correct number, or letter, for your choice.')

            while (answer == str(2)):
                print(Fore.WHITE + Style.BRIGHT+'\nDo you want to see a sample of the raw data?\n')
                main(input('\nPress 1 if Yes.\nPress 2 if no.\nEnter here: '), True)
                memory_usage()
                print(Fore.WHITE+'\nChoose which city would you want for your statistics.\nPress 1 to choose Chicago.\nPress 2 to choose New York.\nPress 3 to choose Washington, DC.\nPress B to go back.')
                city = (input('\nType your choice here: ')).title()

                while (city > str(0) and city < str(4) and len(city) == 1):
                    print(Fore.WHITE+'\nTo see the Most Common Start Station, press 1.\nTo see the Most Common End Station, press 2.\nTo see the Most Common Trip, press 3.\nTo go back, press B.')
                    answer_2 = (input('\nType your choice here: ')).title()
                    menu = 2
                    while (answer_2 > str(0) and answer_2 < str(4) and menu == 2):
                        stations(city, answer_2)
                        menu = 1
                    if (answer_2 == 'B'):
                        break
                    elif (answer_2 != str(1) and answer_2 != str(2) and answer_2 != str(3) and answer_2 != 'B'):
                        print(Fore.RED + '\nType a correct number, or letter, for your choice.')

                if (city == 'B'):
                    break
                elif (city != 'B' and (city < str(1) or city > str(3))):
                    print(Fore.RED + '\nType a correct number, or letter, for your choice.')

            while (answer == str(3)):
                print(Fore.WHITE + Style.BRIGHT+'\nDo you want to see a sample of the raw data?\n')
                main(input('\nPress 1 if Yes.\nPress 2 if no.\nEnter here: '), True)
                memory_usage()
                print(Fore.WHITE+'\nChoose which city would you want for your statistics.\nPress 1 to choose Chicago.\nPress 2 to choose New York.\nPress 3 to choose Washington, DC.\nPress B to go back.')
                city = (input('\nType your choice here: ')).title()
                while (city > str(0) and city < str(4) and len(city) == 1):
                    print(Fore.WHITE+'\nPress 1 to get the Total Travel Time.\nPress 2 to get the Average Travel Time.\nTo go back, press B.')
                    answer_3 = (input('\nType your choice here: ')).title()
                    menu = 3
                    while (answer_3 > str(0) and answer_3 < str(3) and menu == 3):
                        travel(city, answer_3)
                        menu = 1
                    if (answer_3 == 'B'):
                        break
                    elif (answer_3 != str(1) and answer_3 != str(2) and answer_3 != 'B'):
                        print(Fore.RED + '\nType a correct number, or letter, for your choice.')
                if (city == 'B'):
                    break
                elif (city != 'B' and (city < str(1) or city > str(3))):
                    print(Fore.RED + '\nType a correct number, or letter, for your choice.')

            while (answer == str(4)):
                print(Fore.WHITE + Style.BRIGHT+'\nDo you want to see a sample of the raw data?\n')
                main(input('\nPress 1 if Yes.\nPress 2 if no.\nEnter here: '), True)
                memory_usage()
                print(Fore.WHITE+'\nChoose which city would you want for your statistics.\nPress 1 to choose Chicago.\nPress 2 to choose New York.\nPress 3 to choose Washington, DC.\nPress B to go back.')
                city = (input('\nType your choice here: ')).title()
                while (city > str(0) and city < str(3)):
                    print(Fore.WHITE+'\nPress 1 to get the count of each user type.\nPress 2 to get the count of each gender.\nPress 3 to get the earliest, the recent and the most common birthyear of customers.\nPress B to go back.\n')
                    answer_4 = (input('\nType your choice here: ')).title()
                    menu = 3
                    while (answer_4 < str(3) and answer_4 > str(0)):
                        user_info(city, answer_4, 0)
                        break
                    while (answer_4 == str(3) and menu == 3):
                        print(Fore.WHITE+'\nPress 1 to get the earliest birth year.\nPress 2 to get the recent birth year.\nPress 3 to get the most common birth year.\nPress B to go back.')
                        birth_year = (input('\nType your choice here: ')).title()
                        while (birth_year > str(0) and birth_year < str(4) and len(birth_year) == 1):
                            user_info(city, answer_4, birth_year)
                            break
                        if (birth_year == 'B'):
                            break
                        elif (birth_year != 'B' and birth_year != str(1) and birth_year != str(2) and birth_year != str(3)):
                            print(Fore.RED + '\nType a correct number, or letter, for your choice.')
                    if (answer_4 == 'B'):
                        break
                    elif (answer_4 != 'B' and (answer_4 < str(1) or answer_4 > str(3))):
                        print(Fore.RED + '\nType a correct number, or letter, for your choice.')
                while (city == str(3)):
                    print(Fore.YELLOW+'\nWe are sorry to inform you that our database doesn\'t have the birth year and the gender of customer on Washington, D.C\nYou will now get the results for the following question: Count of each user type.')
                    user_info(city,str(1),0)
                    break
                if (city == 'B'):
                    break
                elif (city != 'B' and (city < str(1) or city > str(3))):
                    print(Fore.RED + '\nType a correct number, or letter, for your choice.')
            if (answer == 'Q'):
                start = False
                download = 'Q'
                download_is_starting = False
                break
            elif (answer != 'Q' and (answer < str(1) or answer > str(4))):
                print(Fore.RED + '\nPlease, type a correct number, or letter, for your choice.')

    elif(download == 'Q'):
        start = False
        break
    else:
        print(Fore.RED + '\nPlease, type a correct number, or letter, for your choice.')
        break

memory_usage()
print(Fore.GREEN+'\nThank you for your review! I hope that the code had met your expectations.')

"""
Time statistics and memory statistics are represented in matplotlib.
"""
plt.plot(time_statistics,memory_statistcs)
plt.xlabel('Time (In mm-ss)')
plt.ylabel('Memory Usage (In Mbs)')
plt.tight_layout()
plt.savefig('memory_usage.png')
plt.show()

