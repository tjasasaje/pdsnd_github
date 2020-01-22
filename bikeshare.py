import time
import datetime
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hi there! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = str(input("Enter the name of the city you wish to analyze (Chicago/New York/Washington) :"))
    city = city.lower()
    while city not in ('chicago','new york','washington'):
        city = str(input("Invalid input: Please enter a valid city name (Chicago/New York/Washington) :"))
        city = city.lower()

    print('\nGreat! You chose {}.\n'.format(city.title()))

    # TO DO: get user input for month (all, january, february, ... , june)
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    filter_by = str(input("Do you wish to filter by month, day, both, or not at all? (month/day/both/none) :"))
    filter_by = filter_by.lower()
    while filter_by not in ('month','day','both','none'):
        filter_by = str(input("Invalid input: Please enter a valid filter (month/day/both/none) :"))
        filter_by = filter_by.lower()


    if filter_by == 'both':
       # get month input
       print("\nYou chose to filter by both month and day.\n")
       month = str(input("Please enter the name of the month to filter by (january, february, ... , june): "))
       month = month.lower()
       while month not in ('january','february','march','april','may','june'):
           month = str(input("Invalid input: Please enter a month (january, february, ... , june): "))
           month = month.lower()

       # get day input
       day = str(input("Please enter the day of the week to filter by (monday, tuesday, ... sunday): "))
       day = day.lower()
       while day not in ('monday','tuesday','wednesday','thursday','friday','saturday', 'sunday'):
           day = str(input("Invalid input: Please enter a valid day of the week (monday, tuesday, ... sunday): "))
           day = day.lower()

       print("\nThe results will be shown for {} and {}.\n".format(month.title(), day.title()))


    elif filter_by == 'month':
        print("\nYou chose to filter by month.\n")
        month = str(input("Please enter the name of the month to filter by (january, february, ... , june): "))
        month = month.lower()
        while month not in ('january','february','march','april','may','june'):
            month = str(input("Invalid input: Please enter a month (january, february, ... , june): "))
            month = month.lower()
        print("\nThe results will be shown for {}.\n".format(month.title()))
        day = 'all'

    elif filter_by == 'day':
        print("\nYou chose to filter by day.\n")

        # set month to 'all'
        month = 'all'
        # get day input
        day = str(input("Please enter the day of the week to filter by (monday, tuesday, ... sunday): "))
        day = day.lower()
        while day not in ('monday','tuesday','wednesday','thursday','friday','saturday', 'sunday'):
            day = str(input("Invalid input: Please enter the day of the week (monday, tuesday, ... sunday): "))
            day = day.lower()
        print("\nThe results will be shown for {}.\n".format(day.title()))

    else:
        print("\nYou chose to have no filters.\n")
        month = 'all'
        day = 'all'

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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns

    # filter by month if applicable
    if month != 'all':

        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1


        # month is returned in integers where January=1, December=12
        df['month'] = df['Start Time'].dt.month
        # filter by month to create the new dataframe
        df = df[df['month'] == month]


    # filter by day of week if applicable
    if day != 'all':
        # weekday_name is returned in strings e.g. Monday, Tuesday, etc
        df['day_of_week'] = df['Start Time'].dt.weekday_name
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df, m, d):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month and don't display anything if the user filtered by month anyway
    if m == 'all':
        df['month'] = df['Start Time'].dt.month_name()
        most_common_month = df['month'].mode()[0]
        print('Most common month to travel: {} '.format(most_common_month))


    # Display the most common day of week and don't display anything if the user filtered by day anyway
    if d == 'all':
        df['day_of_week2'] = df['Start Time'].dt.weekday_name
        most_common_day = df['day_of_week2'].mode()[0]
        print('Most common day of week to travel: {} '.format(most_common_day))

    # Display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    most_common_hour = df['hour'].mode()[0]
    print('Most common hour to travel: {} '.format(most_common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    df_c = df.groupby(['Start Station'])['Start Station'].count().reset_index(name='Start_Station_Count')
    get_max = df_c['Start_Station_Count'].max()
    most_popular_start_station = df_c.loc[df_c['Start_Station_Count'] == get_max,'Start Station'].values[0]
    print('Most commonly used start station is:',most_popular_start_station)

    # Display most commonly used end station
    df_c2 = df.groupby(['End Station'])['End Station'].count().reset_index(name='End_Station_Count')
    get_max2 = df_c2['End_Station_Count'].max()
    most_popular_end_station = df_c2.loc[df_c2['End_Station_Count'] == get_max2,'End Station'].values[0]
    print('Most commonly used end station is:',most_popular_end_station)
    print()

    # Display most frequent combination of start station and end station trip
    df_c3 = df.groupby(['Start Station','End Station'])['End Station'].count().reset_index(name='Combo_Count')
    get_max = df_c3['Combo_Count'].max()
    combo_df = df_c3.loc[df_c3['Combo_Count'] == get_max]
    combo_start = str(combo_df['Start Station'].values[0])
    combo_end = str(combo_df['End Station'].values[0])

    print('Most frequent trip is:')
    print(combo_start, '-->', combo_end)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    total_seconds = df['Trip Duration'].sum()
    total_travel_time = str(datetime.timedelta(seconds = int(total_seconds)))
    print('Total travel time:', total_travel_time)
    # Display mean travel time
    mean_seconds = df['Trip Duration'].mean()
    average_travel_time = str(datetime.timedelta(seconds = int(mean_seconds)))
    print('Average travel time:', average_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    df2 = df.groupby(['User Type'])['User Type'].count().reset_index(name='User Count')
    user_list = df2['User Type'].values
    user_ct_list = df2['User Count'].values

    print('*Count of users by type*')
    for i in range(len(user_list)):
            print(user_list[i] + ':',user_ct_list[i])
    print()

    # Display counts of gender
    if city != 'washington':
        df3 = df['Gender']
        df3.fillna('Unknown', inplace = True)
        df3 = df.groupby(['Gender'])['Gender'].count().reset_index(name='Gender Count')
        gender_list = df3['Gender'].values
        gender_ct_list = df3['Gender Count'].values

        print('*Count of users by Gender*')
        for i in range(len(gender_list)):
            print(gender_list[i] + ':',gender_ct_list[i])
        print()
    else:
        print('No Gender information for Washington.')
        print()

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        df4 = df['Birth Year'].dropna()
        earliest_year = df4.min()
        most_recent_year = df4.max()
        most_common_year = df4.mode()
        print('*Year of birth*')
        print('Earliest:', int(earliest_year))
        print('Most recent:', int(most_recent_year))
        print('Most common:', int(most_common_year))
    else:
        print('No Birth Year information for Washington.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
