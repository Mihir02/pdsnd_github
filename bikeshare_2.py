import time
import pandas as pd
import numpy as np

CITY_DATA = {
    "chicago": "chicago.csv",
    "new york city": "new_york_city.csv",
    "washington": "washington.csv",
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    while True:
        city = input(
            "Please enter the city you want to explore: Chicago, New York City or Washington: "
        ).lower()
        if city not in ("chicago", "new york city", "washington"):
            print("Please enter a valid city name.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input(
            "Please enter the month you want to explore: January, February, March, April, May, June or All: "
        ).lower()
        if month not in ("january", "february", "march", "april", "may", "june", "all"):
            print("Please enter a valid month name.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input(
            "Please enter the day of the week you want to explore: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or All: "
        ).lower()
        if day not in (
            "monday",
            "tuesday",
            "wednesday",
            "thursday",
            "friday",
            "saturday",
            "sunday",
            "all",
        ):
            print("Please enter a valid day of the week.")
            continue
        else:
            break

    print("-" * 40)
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
    df = pd.DataFrame(pd.read_csv(CITY_DATA[city]))
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.day_name()

    if month != "all":
        months = ["january", "february", "march", "april", "may", "june"]
        df = df[df["month"] == months.index(month) + 1]

    if day != "all":
        df = df[df["day_of_week"] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\nCalculating The Most Frequent Times of Travel...\n")
    start_time = time.time()

    # display the most common month
    common_month = df["month"].mode()[0]
    print("Most common month:", common_month)

    # display the most common day of week
    common_day = df["day_of_week"].mode()[0]
    print("Most common day of the week:", common_day)

    # display the most common start hour
    df["hour"] = df["Start Time"].dt.hour
    common_hour = df["hour"].mode()[0]
    print("Most common hour:", common_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\nCalculating The Most Popular Stations and Trip...\n")
    start_time = time.time()

    # display most commonly used start station
    Start_Station = df["Start Station"].value_counts().idxmax()
    print("Most Commonly used start station:", Start_Station)

    # display most commonly used end station
    End_Station = df["End Station"].value_counts().idxmax()
    print("Most Commonly used end station:", End_Station)

    # display most frequent combination of start station and end station trip
    Combination_Station = df.groupby(["Start Station", "End Station"]).count()
    print(
        "Most Commonly used combination of start station and end station trip:",
        Start_Station,
        " & ",
        End_Station,
    )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print("-" * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\nCalculating Trip Duration...\n")
    start_time = time.time()

    # display total travel time
    Total_Travel_Time = sum(df["Trip Duration"])
    print("Total travel time:", Total_Travel_Time / 86400, " Days")

    # display mean travel time
    Mean_Travel_Time = df["Trip Duration"].mean()
    print("Mean travel time:", Mean_Travel_Time / 60, " Minutes")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print("-" * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\nCalculating User Stats...\n")
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print("User Types: \n", user_types)

    # Display counts of gender
    try:
        gender_types = df["Gender"].value_counts()
        print("\nGender Types:\n", gender_types)
    except KeyError:
        print("\nGender Types:\nNo data available for this month.")

    # Display earliest, most recent, and most common year of birth
    try:
        Earliest_Year = df["Birth Year"].min()
        print("\nEarliest Year:", Earliest_Year)
    except KeyError:
        print("\nEarliest Year:\nNo data available for this month.")

    try:
        Most_Recent_Year = df["Birth Year"].max()
        print("\nMost Recent Year:", Most_Recent_Year)
    except KeyError:
        print("\nMost Recent Year:\nNo data available for this month.")

    try:
        Most_Common_Year = df["Birth Year"].value_counts().idxmax()
        print("\nMost Common Year:", Most_Common_Year)
    except KeyError:
        print("\nMost Common Year:\nNo data available for this month.")

    print(f"\nThis took {(time.time() - start_time)} seconds.")
    print("-" * 40)


def view_data(df):
    """Displays 5 rows of data upon request by the user."""
    view_data = input(
        "\nWould you like to view 5 rows of individual trip data? Enter yes or no\n"
    ).lower()
    start_loc = 0
    while view_data == "yes":
        print(df.iloc[start_loc : start_loc + 5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart = input("\nWould you like to restart? Enter yes or no.\n")
        if restart.lower() != "yes":
            break


if __name__ == "__main__":
    main()
