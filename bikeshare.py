import pandas as pd
import time

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
months = ['january', 'february', 'march', 'april', 'may', 'june']
days = ['saturday', 'sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday']


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    city = input("Please enter the name of the city to analyze: ").lower()
    while city not in CITY_DATA:
        city = input("From (chicago, new york city, washington). \n"
                     "Please enter a valid name of the city to analyze: ").lower()

    # TO DO: get user input for month (all, january, february, ... , june)

    month = input('Please enter the the month to filter by, or "all" to apply no month filter: ').lower()
    while (month != 'all') and (month not in months):
        month = input('From (all, january, february, ... , june). \n'
                      'Please enter the the month to filter by, or "all" to apply no month filter: ').lower()
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)

    day = input('Please enter name of the day of week to filter by, or "all" to apply no day filter: ')
    while (day != 'all') and (day not in days):
        day = input('From (saturday, sunday ,monday, tuesday, wednesday, thursday, friday)\n'
                    'Please enter name of the day of week to filter by, or "all" to apply no day filter: ')

    print('-' * 40)
    return CITY_DATA[city], month, day


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
    df = pd.read_csv(city)

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month
    df['Day of week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['Month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['Day of week'] == day.title()]

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['Month'].mode()[0]
    print('Most Popular Month:', months[popular_month-1])

    # TO DO: display the most common day of week
    popular_day = df['Day of week'].mode()[0]
    print('Most Popular Day:', popular_day)

    # TO DO: display the most common start hour
    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_ssn = df['Start Station'].mode()[0]

    # TO DO: display most commonly used end station
    common_esn = df['End Station'].mode()[0]

    # TO DO: display most frequent combination of start station and end station trip
    common_sesn = (df['Start Station'] + " to " + df['End Station']).mode()[0]

    print("Most common start station : {}, end station : {}, and combination : {} .".format(
        common_ssn, common_esn, common_sesn))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_tt = df['Trip Duration'].sum()
    # TO DO: display mean travel time
    mean_tt = int(df['Trip Duration'].mean())

    print("Total travel time : {} hrs, {} mins, {} secs".format(total_tt//3600, (total_tt//60)-(total_tt//3600)*60,
                                                                total_tt % 60))
    print("Mean travel time : {} hrs, {} mins, {} secs".format(mean_tt//3600, (mean_tt//60)-(mean_tt//3600)*60,
                                                               mean_tt % 60))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    # print value counts for each user type
    user_types = df['User Type'].value_counts()
    print(user_types)

    if city == 'chicago.csv':
        # TO DO: Display counts of gender
        # print value counts for each gender
        user_genders = df['Gender'].value_counts()
        print(user_genders)

    if city != 'washington.csv':
        # TO DO: Display earliest, most recent, and most common year of birth
        earliest = df['Birth Year'].min()
        recent = df['Birth Year'].max()
        common = df['Birth Year'].mode()[0]

        print("Earliest year of birth : {}, most recent : {}, and most common {}.".format(earliest, recent, common))
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-' * 40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        view_data = input('\nWould you like to view first 5 rows of individual trip data? Enter yes or no\n').lower()
        while view_data not in ['yes', 'no']:
            view_data = input('\nPlease Enter A Valid Response!\nWould you like to view first 5 rows of individual trip data? Enter yes or no\n').lower()

        if view_data == 'yes':
            i = 0
            print(df[i:i+5].iloc[:, 1:-3])
            while view_data == 'yes':
                view_data = input('\nDo you want to see the next 5 rows of data?\n').lower()

                while view_data not in ['yes', 'no']:
                    view_data = input('\nPlease Enter A Valid Response!\nWould you like to view first 5 rows of individual trip data? Enter yes or no\n').lower()

                i += 5
                print(df[i:i+5].iloc[:, 1:-3])
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        while restart not in ['yes', 'no']:
            restart = input('\nPlease Enter A Valid Response!\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            break


if __name__ == "__main__":
    main()
