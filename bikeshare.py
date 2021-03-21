import time
import pandas as pd
import numpy as np

import datetime as dt
import click

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

months = ('january', 'february', 'march', 'april', 'may', 'june')

weekdays = ('sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
            'saturday')

def get_choice(command,choices=('yes','no')):
    while True:
        action = input(command).lower().strip()
        if action == 'end':
            raise SystemExit
        elif action =='all':
            break
        elif ',' not in action:
            if action in choices:
                break
        # Filter out commmas from action:
        elif ',' in action:
            act = [i.strip().lower() for i in action.split(',')]
            if list(filter(lambda x: x in choices, act)) == act:
                break
        else:
            command = "\nPlease enter a valid option"
    return action
    
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    print('Warning! Input data in the convenient format.')
    while True:
        # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
        city = get_choice('\nEnter the city name choosing among (chicago, new york city, washington) and use commas to list more than a name.\n' 
                          ,CITY_DATA.keys())
    
        # TO DO: get user input for month (all, january, february, ... , june)
        month = get_choice( "\nChoose from January to June, for what month(s) do you want do filter data? Use 'all' for all months.\n>" ,months)
    
        # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        # The choice should be recieved as a number too:
        day = get_choice("\nNow choose for what weekday(s) do you want do filter bikeshare data? choose 'all' "
                         "for all days.\n>",weekdays)
    
        confirmation = get_choice("\nConfirm that you would like to apply "
                              "the following filter(s) to the bikeshare data."
                              "\n\nCity: {}\nMonth: {}\nWeekday(s)"
                              ": {} \n\n [yes] Yes\n [no] No\n\n>"
                              .format(city, month, day))
        if confirmation == 'yes':
            break
        else:
            print('Re-enter the data again !')
    
    print('-'*40)
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
    start_time = time.time()
    ## In case of more than a city we need mapping 
    if type(city) == list:
        df = pd.concat(map(lambda city: pd.read_csv(CITY_DATA[city]), city),sort=True)

        try:
            df = df.reindex(columns=['Unnamed: 0', 'Start Time', 'End Time','Trip Duration', 'Start Station',
                                     'End Station', 'User Type', 'Gender','Birth Year'])
        except:
            pass
    else:
        # In case of city is chosen
        df = pd.read_csv(CITY_DATA[city])
    
    # Finding columns needed
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['Month'] = df['Start Time'].dt.month
    df['Weekday'] = df['Start Time'].dt.weekday_name
    df['Start Hour'] = df['Start Time'].dt.hour
    
    ## Mapping months
    if month != 'all':
        if type(month) == list:
            df = pd.concat(map(lambda month: df[df['Month'] == (months.index(month)+1)], month)) 
        else:
            df = df[df['Month'] == (months.index(month)+1)]
    ## Mapping days
    if day != 'all':
       # if type(day) == list:
        if isinstance(day, list):
            df = pd.concat(map(lambda day: df[df['Weekday'] == (day.title())], day))
        else:
            df = df[df['Weekday'] == day.title()]
    
    print("\nThis took {} seconds.".format((time.time() - start_time)))
    return df    

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    df['Month'].head()
    most_common_month = df['Month'].mode()[0]
    print('The month with the most travels is: ',str(months[most_common_month-1]).title() , '.')

    # TO DO: display the most common day of week
    most_comon_day = df['Weekday'].mode()[0]
    print('The day with the most travels is: ' , str(most_comon_day) , '.')

    # TO DO: display the most common start hour
    most_comon_start = df['Start Hour'].mode()[0]
    print('The hour with the most starts is: ' , str(most_comon_start) , '.')
    # Time is in seconds only !
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return 0


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_common_start_stat = df['Start Station'].mode()[0]
    print("The most common start station is: ", str(most_common_start_stat))

    # TO DO: display most commonly used end station
    most_common_end_stat = df['End Station'].mode()[0]
    print("The most common end station is: ", str(most_common_end_stat))

    # TO DO: display most frequent combination of start station and end station trip
    df['Start End Comb'] = df['Start Station'] + ' ' + df['End Station']
    most_common_comb = df['Start End Comb'].mode()[0]
    print("The most frequent combination of start station and end station trip: ", str(most_common_comb))
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()

    total_travel_time = (str(int(total_travel_time//86400)) + 'days ' +  
                         str(int((total_travel_time % 86400)//3600)) + 'hours ' +
                         str(int(((total_travel_time % 86400) % 3600)//60)) +'minutes ' +
                         str(int(((total_travel_time % 86400) % 3600) % 60)) +'seconds')
    # TO DO: display mean travel time
    print('The total travel time is : ' , total_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts().to_string()
    print('User types:',user_types)

    # TO DO: Display counts of gender
    try:
        gender_distribution = df['Gender'].value_counts().to_string()
        print('Gender counts:',gender_distribution)
    except KeyError:
        print("There is no data of user genders for this city")
    
    # TO DO: Display earliest, most recent, and most common year of birth
    try:    
        earliest_year = str(int( df['Birth Year'].min()))
        print('Eearliest year of birth', earliest_year)
    
        recent_year = str(int( df['Birth Year'].max()))
        print('Most recent year of birth', recent_year)    

        commont_year = str(int( df['Birth Year'].mode()[0]))
        print('Most coomon year of birth', commont_year)    
    except:        
        print("We're sorry! There is no data of user birth years for this city" )
   
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return 0

def show_data(df):
    i = 5
    choice = get_choice( "\nWould you like to show five rows of the targeted database.\n>"
                            ": \n\n [yes] Yes\n [no] No\n\n>")
    while True:
        if choice == 'yes' or choice =='YEs':
            print(df.head(i))
            i += 5
        else: 
            break
        choice = get_choice( "\nWould you like to show more five rows of the targeted database.\n>"
                            ": \n\n [yes] Yes\n [no] No\n\n>")    
    return 0    

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        df = load_data(city, month, day)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
