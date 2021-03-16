import time
import datetime
import pandas as pd
import numpy as np
import os

"""
Readme references
-------------------------------------------------------------------------------------------
Udacity material course.
Classroom presentations.
https://docs.python.org/es/3/library/datetime.html
https://www.geeksforgeeks.org/python-get-key-from-value-in-dictionary/
https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.dt.weekday.html
https://stackoverflow.com/questions/29645153/remove-name-dtype-from-pandas-output
https://docs.python.org/3/tutorial/errors.html
https://stackoverflow.com/questions/19828822/how-to-check-whether-a-pandas-dataframe-is-empty
https://stackoverflow.com/questions/15943769/how-do-i-get-the-row-count-of-a-pandas-dataframe
https://stackoverflow.com/questions/517970/how-to-clear-the-interpreter-console

"""

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

City_string = ", ".join( [ City_key for City_key , City_value in CITY_DATA.items()] ) 

Months = {'all': 0, 'january': 1, 'february': 2, 'march': 3, 'april': 4, 'may': 5, 'june': 6, 'july': 7, 'august': 8, 'september': 9, 'october': 10, 'november': 11, 'december':12 }
Months_string = ", ".join( [ str(Month_value) + ': ' + Month_key for Month_key , Month_value in Months.items()] ) 

Days = {'all': 0, 'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'sunday': 7} 
Days_string = ", ".join( [ str(Day_value) + ': ' + Day_key for Day_key , Day_value in Days.items()] ) 



def cls():
    os.system('cls' if os.name=='nt' else 'clear')

def print_rows(df):

    while True:

        show_data = input('\nWould you like to navigate over dataframe (y/n):')
        
        if show_data == 'n':
            break
        else:

            pos = 0
            next = 'n'

            try:
                qty_rows = int(input('\nPlease input quantity of rows to navigate. Number between (10..10000):'))

                if  10 <= qty_rows <= 10000:

                    if qty_rows > df.shape[0]:
                        qty_rows = df.shape[0]

                    while next != 'e' and pos < df.shape[0]:
                        print('-'*100)

                        if pos + qty_rows > df.shape[0]:
                            qty_rows =  df.shape[0] - pos

                        print('\nShowing rows from {} to {}:\n'.format(pos, pos + qty_rows))
                        print(df.iloc[pos : pos + qty_rows , : ])
                        next = input("Press Enter to continue or (e) to exit: ")

                        if pos + qty_rows < df.shape[0]:
                            pos += qty_rows
                        else:    
                            pos = df.shape[0]   
                            qty_rows = pos
                            
                


                else:
                    break    
            except Exception as e:
                print('Please input a valid number:{}', format(e))            


def get_month_name(month_number):

    if month_number == 0:
        return 'All'
    else:
        return list(Months.keys())[list(Months.values()).index(month_number)]

def get_day_name(day_number):
    if day_number == 0:
        return 'All'
    else:    
        return list(Days.keys())[list(Days.values()).index(day_number)]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('This is the Rodrigo Contreras Vielma APP (contrerasvielma@gmail.com), enjoy the information with Python:')
    print('-'*100)

    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input('\nInput city to analysis ({})=> '.format(City_string))
        
        if city.lower() in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('please input a valid city (chicago, new york city, washington)')

    # TO DO: get user input for month (all, january, february, ... , june)

  
    while True:
        Month_input = input('\nInput a month:\n' + Months_string + "\n=>").lower().strip()

        if Month_input in Months:
            month = int(Months.get(Month_input, -1))
            break

        elif Month_input.isnumeric() and ( 0 <= int(Month_input) <= 12):
            month = int(Month_input)
            break

        else:
            print('Please, input a correct month name or month number (0: All)')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)


    while True:
        Day_input = input('\nInput a day:\n' + Days_string + "\n=> ").lower().strip()

        if Day_input in Days:
            day = int(Days.get(Day_input, -1))
            break

        elif Day_input.isnumeric() and ( 0 <= int(Day_input) <= 7):
            day = int(Day_input)
            break

        else:
            print('Please, input Day name or Day number (0: All)')


    print('\n\nwe are preparing analysis to the following parameters, City: {0}, Month: {1}, Day: {2}'.format(city, get_month_name(month), get_day_name(day)))
    print('-'*100)

    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    df = pd.read_csv(CITY_DATA[city])

    print('\nHead information of dataframe:\n')
    print(df.head())  # start by viewing the first few rows of the dataset!
  

    print('\nSize of original dataframe: ', df.size)
    print('Total row count of original dataframe: ', df.shape[0])
    print('-'*100)
    input("Press Enter to continue...")


    df.info(verbose=True)

    df['Start Time'] = pd.to_datetime(df['Start Time'], format="%Y-%m-%d %H:%M:%S")

    # filter by month if applicable
    if month != 0:
        df = df[df['Start Time'].dt.month == month]
    
    # filter by day if applicable, remember weekday: 0 is Monday, 1: tuesday ...
    if day != 0:
        df = df[df['Start Time'].dt.weekday == day - 1]


    print('\nSize of dataframe with filters: ', df.size)
    print('Filtered Row count of dataframe: ', df.shape[0])
    print('-'*100)
    input("Press Enter to continue...")


    
#    print(df.head()) 
#     display(df.describe())
#    print(df.columns)

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month

    try:
        df['month'] = df['Start Time'].dt.month

        popular_month = df['month'].mode()[0]

        #print('Most Popular Month:', popular_month)

        print('Most Popular Month:', get_month_name(popular_month))
  
    except Exception as e:    
        print('Error to display the most common month. Error occurred: {}'.format(e))   
   


    # TO DO: display the most common day of week

    try:
        df['weekday'] = df['Start Time'].dt.weekday

        popular_weekday = df['weekday'].mode()[0]

        #print('Most Popular Weekday:', popular_weekday)
        print('Most Popular Weekday:', get_day_name(popular_weekday + 1))

    except Exception as e:

        print('Error to display the most common day of week. Error occurred: {}'.format(e))   

    # TO DO: display the most common start hour

    try:
        df['hour'] = df['Start Time'].dt.hour

        popular_hour = df['hour'].mode()[0]

        print('Most Popular Hour:', popular_hour)

    except Exception as e:

        print('Error to display the most common start hour. Error occurred: {}'.format(e))  


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)
    input("Press Enter to continue...")


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station

    try:
        #popular_StartStation = df['Start Station'].mode()[0]  -- is better the following sentence if we have two or more modes.

        popular_StartStation = df['Start Station'].mode().iloc[ : df['Start Station'].mode().shape[0]].to_string(index=False)

        print('Most Popular Start Station:', popular_StartStation)

    except Exception as e:

        print('Error to display the most common used start station. Error occurred: {}'.format(e))  

    # TO DO: display most commonly used end station

    try:
        #popular_EndStation = df['End Station'].mode()[0]  -- is better the following sentence if we have two or more modes.

        popular_EndStation = df['End Station'].mode().iloc[ : df['End Station'].mode().shape[0]].to_string(index=False)

        print('Most Popular End Station:', popular_EndStation)

    except Exception as e:

        print('Error to display the most common used end station. Error occurred: {}'.format(e))  

    # TO DO: display most frequent combination of start station and end station trip

    try:
        df['StartEndStation'] = df['Start Station'] + ' - ' + df['End Station']

        print('Quantity of mode according parameters:', df['StartEndStation'].mode().shape[0])
    
        popular_StartEndStation = df['StartEndStation'].mode().iloc[ : df['StartEndStation'].mode().shape[0]].to_string(index=False)

        print('Most Popular Start to End Station:\n', popular_StartEndStation)


    except Exception as e:

        print('Error to display the most frequent combination of start station and end station trip. Error occurred: {}'.format(e)) 

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)
    input("Press Enter to continue...")

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time

    try:

        total_travel_time = df['Trip Duration'].sum()

        print('Total travel time:', total_travel_time)

    except Exception as e:

        print('Error to display total travel time. Error occurred: {}'.format(e))  


    # TO DO: display mean travel time

    try:

        mean_travel_time = df['Trip Duration'].mean()

        print('Mean travel time:', mean_travel_time)

    except Exception as e:

        print('Error to display mean travel time. Error occurred: {}'.format(e))  

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)
    input("Press Enter to continue...")

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types

    try:

        count_user_types = df['User Type'].value_counts().to_string()


        print('\nCounts of user types:\n', count_user_types)

    except Exception as e:

        print('Error to display counts of user types. Error occurred: {}'.format(e))  


    # TO DO: Display counts of gender

    try:
        gender_user_types = df['Gender'].value_counts().to_string()

        print('\nGender of user types:\n', gender_user_types)

    except Exception as e:

        print('Error to display counts of gender. Error occurred: {}'.format(e))  

    # TO DO: Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*100)


def main():
    while True:

        cls()

        city, month, day = get_filters()
    
        df = load_data(city, month, day)

        if not df.empty:
            time_stats(df)

            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)
            print_rows(df)
        else:
            print('There is no data according to the entered parameters. It is not possible to analyze information.')    

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() in ('no', 'n'):
            break


if __name__ == "__main__":
	main()
