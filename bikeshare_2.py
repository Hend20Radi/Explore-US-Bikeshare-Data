# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 11:39:49 2020

@author: radi
"""
import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

#Assigning important variables with a "global scope" which will be used in our functions
city_dict = {"a": "chicago", "b": "new york city", "c": "washington"}
months = {"1": "january", "2": "february", "3": "march", "4": "april", "5": "may", "6": "june", "n": "no filter by month"}
days = {"1": "monday", "2": "tuesday", "3": "wednesday", "4": "thursday", "5": "friday", "6": "saturday", "7": "sunday", "n": "no filter by day"}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        try:
            city = input("Enter:\n(a) for Chicago,\n(b) for New York City,\n(c) for Washington.\n")
            #Handling some user-input errors (typos)
            if city.lower() in city_dict.keys():
                print("You chose {}.".format(city_dict[city.lower()].title()))
                break
            else:
                print("Oops! Something went wrong!\nAre you sure you entered a valid letter?\nAre you sure you entered the letter in lowercase?\nPlease try again.")
        #Handling expected exception
        except KeyboardInterrupt:
            print("KeyboardInterrupt! Please try again.")
        finally:
            print("*The second step is to filter data by month (if you want).")


    # get user input for month (no filter, january, february, ... , june)
    while True:
        try:
            month = input("Now enter the number corresponding to the month that you want\nOR\ntype (n) if you don't want to filter by month.\n"
                          "-January: 1\n-February: 2\n-March: 3\n-April: 4\n-May: 5\n-June: 6\n-No Filter By Month: n\n")
            #Handling some user-input errors (typos)
            if month.lower() in months.keys():
                print("You chose \'{}\'.".format(months[month.lower()].title()))
                break
            else:
                print("Oops! Something went wrong!\nAre you sure you entered a valid number?\nAre you sure you entered the letter (n) in lowercase?\nPlease try again.")
        #Handling expected exception
        except KeyboardInterrupt:
            print("KeyboardInterrupt! Please try again.")
        finally:
            print("*The third and final step is to filter data by day (if you want).")

    # get user input for day of week (no filter, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("Now enter the number corresponding to the day that you want\nOR\ntype (n) if you don't want to filter by day.\n"
                        "-Monday: 1\n-Tuesday: 2\n-Wednesday: 3\n-Thursday: 4\n-Friday: 5\n-Saturday: 6\n-Sunday: 7\n-No Filter By Day: n\n")
            #Handling some user-input errors (typos)
            if day.lower() in days.keys():
                print("You chose \'{}\'.".format(days[day.lower()].title()))
                break
            else:
                print("Oops! Something went wrong!\nAre you sure you entered a valid number?\nAre you sure you entered the letter (n) in lowercase?\nPlease try again.")
        #Handling expected exception
        except KeyboardInterrupt:
            print("KeyboardInterrupt! Please try again.")
        finally:
            print("*Kindly, don't forget to rate our system at the end :)")           

    print('-'*40)
    return city, month, day

city, month, day = get_filters()

#Using results from "get_filters" function to assign some variables with "global scope" that we will use in other functions
city = city_dict[city.lower()]
month = months[month.lower()]
day = days[day.lower()]
print(city.title())
print(month.title())
print(day.title())

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
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'no filter by month':
        # use the index of the months list to get the corresponding int
        months_list = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months_list.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'no filter by day':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

df = load_data(city, month, day)

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    df["month"] = df["Start Time"].dt.month
    popular_month = str(df["month"].mode()[0])
    popular_month = months[popular_month]
    
    # display the most common day of week
    df["day_of_week"] = df["Start Time"].dt.day_name()
    popular_day = df["day_of_week"].mode()[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    return print("The most frequent times of travel are on:\nmonth '{}',\nday '{}',\nhour '{}'.".format(popular_month.title(), popular_day, popular_hour))
    
time_stats(df)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start = df["Start Station"].mode()[0]

    # display most commonly used end station
    common_end = df["End Station"].mode()[0]
    
    # display most frequent combination of start station and end station trip
    common_combination = (df["Start Station"] + df["End Station"]).mode()[0]
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    return print ("The most commonly used start station is '{}'.\nThe most commonly end station is '{}'.\n"
                  "The most frequent combination of start station and end station trip is '{}'.\n".format(common_start, common_end, common_combination))
      
station_stats(df)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_time_s = df["Trip Duration"].sum()
    total_time_h = total_time_s / (60*60)

    # display mean travel time
    average_time_s = df["Trip Duration"].mean()
    average_time_h = average_time_s / (60*60)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return print("Total travel time in seconds = {}\nand in hours = {}.\nAverage travel time in seconds = {}\nand in hours = {}.\n".format(total_time_s, total_time_h, average_time_s, average_time_h))

trip_duration_stats(df)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()

    # Display counts of gender
    if city == "chicago" or city == "new york city":
        gender_count = df["Gender"].value_counts()
        
        # Display earliest, most recent, and most common year of birth
        earliest_birth = df["Birth Year"].min()
        recent_birth = df["Birth Year"].max()
        common_birth = df["Birth Year"].mode()[0]
    else:
        gender_count = "There is no data for it"
        
        earliest_birth = "There is no data for it"
        recent_birth = "There is no data for it"
        common_birth = "There is no data for it"

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    return print("Counts of 'user type' =\n{}.\nCounts of 'gender' =\n{}.\n"
                 "The earliest year of birth = {}.\nThe most recent year of birth = {}.\nThe most common year of birth = {}.\n".format(user_types, gender_count, earliest_birth, recent_birth, common_birth))

user_stats(df)

def first_raw_data():
    """Displays the first 5 raws of the raw data."""
    
    answer = ["yes", "no"]
    while True:
        try:
            answer_1 = input("Whould you like to see 5 raws of the raw data without any filtering or statistics?\n"
                             "Enter (yes) or (no).\n")
            #Handling some user-input errors (typos)
            if answer_1.lower() not in answer:
                print("Please try again and make sure you enter (yes) or (no).")
                answer_1 = input("Whould you like to see another 5 raws of the raw data without any filtering or statistics?\n"
                                 "Enter (yes) or (no).\n")
                
            #Displays the first 5 raws
            elif answer_1.lower() == "yes":
                data = pd.read_csv(CITY_DATA[city])
                print(data.head())
                break
                    
            #Don't display any raw data
            elif answer_1.lower() == "no":
                print("Thank you. We hope you like our system :)")
                break
        #Handling expected exception
        except KeyboardInterrupt:
            print("KeyboardInterrupt! PLease try again.")
    return answer_1

answer_1 = first_raw_data()

def raw_data():
    """"
    Displays 5 rows of the data at a time (starting from the sixth row),
    then ask the user if he/she would like to see 5 more rows of the data.
    It continue prompting and printing the next 5 rows at a time until the user
    chooses "no".
    
    
    local variables:
    count -- Each time the user enter "yes", "count" is increased by 5.
    answer -- a list of two strings, "yes" and "no", that help us in handling errors.
    """
    
    count = 0
    answer = ["yes", "no"]
    if answer_1.lower() != "no":
        answer_2 = input("Whould you like to see another 5 raws of the raw data without any filtering or statistics?\n"
                             "Enter (yes) or (no).\n")
        while True:
            try:
                #Handling some user-input errors (typos)
                if answer_2.lower() not in answer:
                    print("Please try again and make sure you enter (yes) or (no).")
                    answer_2 = input("Whould you like to see another 5 raws of the raw data without any filtering or statistics?\n"
                                     "Enter (yes) or (no).\n")
                #Displays 5 raws at a time (starting from the sixth raw)
                elif answer_2.lower() == "yes":
                    count += 5
                    data = pd.read_csv(CITY_DATA[city])
                    print(data.iloc[0 + count : 5 + count])
                    answer_2 = input("Whould you like to see another 5 raws of the raw data without any filtering or statistics?\n"
                                     "Enter (yes) or (no).\n")
            
                #Don't display raw data anymore
                elif answer_2.lower() == "no":
                    print("Thank you. We hope you like our system :)")
                    break
            #Handling expected exception
            except KeyboardInterrupt:
                print("KeyboardInterrupt! Please try again.")

raw_data()
        
def main():
    """"Ask the user if he want to restart."""
    
    while True:
        try:
            restart = input('\nWould you like to restart? Enter (yes) or (no).\n')
            if restart.lower() == "yes":
                global city, month, day
                city, month, day = get_filters()
                city = city_dict[city.lower()]
                month = months[month]
                day = days[day]
                
                print(city.title())
                print(month.title())
                print(day.title())
                
                df = load_data(city, month, day)
                time_stats(df)
                station_stats(df)
                trip_duration_stats(df)
                user_stats(df)
                global answer_1
                answer_1 = first_raw_data()
                raw_data()
            elif restart.lower() == "no":
                print("\nHow would you rate our system?")
                break
            #Handling some user-input errors (typos)
            elif (restart.lower()) != "yes" and (restart.lower()) != "no":
                print("Something went wrong! Please try again")
        #Handling expected exception
        except KeyboardInterrupt:
            print("KeyboardInterrupt! Please try again.")

if __name__ == "__main__":     
    main()
    
#dictionaries to be used in "user_rating()" function
rating = {"1": "Bad", "2": "Ok", "3": "Good", "4": "Great", "5": "Excellent"}
comment = {"1": "Sorry for that! We will work on improving the system.", "2": "Sad! We will work on improving the system.",
           "3": "We will work on the system to make it better.", "4": "Oh! Thank you.",
           "5": "Really thank you! Your pleasure is our goal."}

def user_rating():
    """"Ask the user to rate the system and suggest improvements."""
    
    while True:
        try:
            rate = int(input("Please enter:\n(1) for 'Bad'\n(2) for 'Ok'\n(3) for 'Good'\n(4) for 'Great'\n(5) fo 'Excellent'\n"))
            #Handling some user-input errors (typos)
            if rate in list(range(1,6)):
                print("{}: {}.\n{}".format(str(rate), rating[str(rate)], comment[str(rate)]))
                improvement = input("\n(Optional) Suggest improvements...\nOR\nhit 'ENTER'\n")
                break
            else:
                print("Something went wrong! Please try again.")
        #Handling expected exception
        except KeyboardInterrupt:
            print("KeyboardInterrupt! Please try again.")
    return print("\nUS Bike-Share System.")

user_rating()