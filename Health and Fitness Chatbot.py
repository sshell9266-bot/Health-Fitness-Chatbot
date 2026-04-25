# Health and Fitness Chatbot
# This chatbot helps users track their weight, view progress, get diet suggestions, receive workout recommendations, log workouts, and log water intake.

# The chatbot uses CSV files to store data for diets, workouts, weight logs, workout logs, and water intake logs. It provides a menu-driven interface for users to interact with the chatbot and manage their health and fitness goals effectively.
from cProfile import label
import pandas as pd
import os

# Define file paths for data storage
FILES = {
    'diet': 'diets.csv',
    'water': 'water_log.csv',
    'workout': 'workouts.csv',
    'weight': 'weight_log.csv',
    'workout_log': 'workout_log.csv'
}

# Function to load data from CSV files, returns an empty DataFrame if the file does not exist
def load_data(name):
    if os.path.exists(FILES[name]):
        return pd.read_csv(FILES[name])
    return pd.DataFrame()

#Function to save data to CSV files
def save_data(df, name):
    df.to_csv(FILES[name], index=False)

# Function to add a new entry to a DataFrame and return the updated DataFrame
def add_entry(df, entry_dict):
    return pd.concat([df, pd.DataFrame([entry_dict])], ignore_index=True)

# Welcome user and ask for their name then greets them with a welcome message.
user_name = input("Welcome to the Health and Fitness Chatbot! Please enter your name: ")
print("Hello " + user_name + " and welcome to the Health & Fitness Chatbot! Let's work toward your health and fitness goals.")

#Function to display the main menu options to the user.
def show_menu():
    print("\nPlease choose an option:")
    print("1. Log weight")
    print("2. View weight progress")
    print("3. Get diet suggestions")
    print("4. Add new diet")
    print("5. Get workout suggestions")
    print("6. Add an exercise")
    print("7. Log workout")
    print("8. View workout log")
    print("9. Log water intake")
    print("10. View water intake log")
    print("11. Exit")

# Function to log the user's weight with error handling for invalid input.
def log_weight():
    try:
        weight = float(input("Please enter your current weight (in lbs): "))
        date = input("Please enter the date (YYYY-MM-DD): ")
        weight_log = load_data('weight')
        new_entry = {'date': date, 'weight': weight}
        updated_log = add_entry(weight_log, new_entry)
        save_data(updated_log, 'weight')
    except ValueError:
        print("Invalid input. Please enter a number.")
        return
    print("Weight logged successfully!")

# Function to view the user's weight progress by displaying all logged weights and calculating the difference between the first and last entry, with error handling for no entries or only one entry.
def view_weight_progress():
    weight_log = load_data('weight')
    if weight_log.empty:
        print("No weight entries yet. Please log your weight first.")
        return
    else:
        print("Your logged weights:")
        for i, row in weight_log.iterrows():
            print(f"{row['date']}: {row['weight']} lbs")
        if len(weight_log) > 1:
            difference = weight_log.iloc[-1]['weight'] - weight_log.iloc[0]['weight']
            if difference < 0:
                print("You have lost", abs(difference), "lbs since your first entry.")
            elif difference > 0:
                print("You have gained", difference, "lbs since your first entry.")
            else:
                print("Your weight has stayed the same since your first entry.")
        else:
            print("Only one weight entry found. Log more weights to see progress.")

#Function to get diet suggestions based on the user's input for diet type or restriction. It checks if the input exists in the diet_plans dictionary and displays the corresponding foods and explanations.
def get_diet_plan():
    diet_data = load_data('diet')
    print("Available diet options:")
    for diet in diet_data['name']:
        print("- " + diet)
    diet_choice = input("Please enter your diet type or restriction: ").strip().lower()

    if diet_choice in diet_data['name'].str.lower().values:
        diet_info = diet_data[diet_data['name'].str.lower() == diet_choice].iloc[0]
        print("Foods to include in a " + diet_choice + " diet:")
        print(", ".join(diet_info['foods'].split(';')))
        print("Explanation:", diet_info['explanation'])
    else:
        print("Diet option not available")

#Function to add a new diet plan to the diet CSV file by taking user input for diet type, foods, and explanation, then saving the updated data back to the CSV file.
def add_diet_plan():
    diet_data = load_data('diet')
    diet_type = input("Enter the diet type: ")
    foods = input("Enter the foods to include (separated by semicolons): ")
    explanation = input("Enter an explanation for this diet: ")
    new_entry = {'name': diet_type, 'foods': foods, 'explanation': explanation}
    updated_diet_data = add_entry(diet_data, new_entry)
    save_data(updated_diet_data, 'diet')
    print("Diet plan added successfully!")

# Function to get workout suggestions based on the user's input for fitness goal and subcategory. 
# It checks if the input exists in the workout CSV file and displays the corresponding exercises.
def get_workout_suggestions():
    workout_data = load_data('workout')
    goal = input("Please enter your fitness goal (strength, cardio, flexibility): ").strip().lower()
    workout_data['category'] = workout_data['category'].str.lower()

    if goal in workout_data['category'].values:
        goal_df = workout_data[workout_data['category'] == goal]
        subcategories = goal_df['subcategory'].unique()
        print("\nAvailable subcategories:")
        print(", ".join(subcategories))
        subcategory = input("Choose a subcategory: ").strip().lower()
        goal_df['subcategory'] = goal_df['subcategory'].str.lower()

        if subcategory in goal_df['subcategory'].values:
            final_df = goal_df[goal_df['subcategory'] == subcategory]

            if final_df.empty:
                print("No exercises found for this subcategory.")
                return

            exercises = final_df['exercise'].iloc[0]
            print(f"\nRecommended exercises for {goal} ({subcategory}):")
            print(", ".join(exercises.split(';')))
        else:
            print("Subcategory not available for this goal.")
    else:
        print("Fitness goal not available.")

#Function to add a new exercise to the workout CSV file by taking user input for category, subcategory, and exercise, then saving the updated data back to the CSV file.
# It includes error handling for invalid categories and subcategories, as well as empty exercise input.
def add_exercise():
    workout_data = load_data('workout')

    CATEGORIES = ["strength", "cardio", "flexibility"]

    SUBCATEGORIES = {
        "strength": ["upper body", "lower body", "core", "full body"],
        "cardio": ["endurance", "hiit", "low impact"],
        "flexibility": ["static", "dynamic", "mobility"]
    }

    print("Available categories:")
    print(", ".join(CATEGORIES))
    category = input("Choose a category: ").strip().lower()

    if category not in CATEGORIES:
        print("Invalid category.")
        return

    print("\nAvailable subcategories:")
    print(", ".join(SUBCATEGORIES[category]))
    subcategory = input("Choose a subcategory: ").strip().lower()

    if subcategory not in SUBCATEGORIES[category]:
        print("Invalid subcategory.")
        return

    new_exercise = input("Enter exercise: ").strip()

    if not new_exercise:
        print("Exercise cannot be empty.")
        return

    workout_data['category'] = workout_data['category'].str.lower()
    workout_data['subcategory'] = workout_data['subcategory'].str.lower()

    match = (workout_data['category'] == category) & (workout_data['subcategory'] == subcategory)

    if not match.any():
        print("No matching row found in CSV.")
        return

    idx = workout_data[match].index[0]
    existing = workout_data.at[idx, 'exercise']

    if pd.isna(existing) or existing.strip() == "":
        updated = new_exercise
    else:
        updated = existing + ";" + new_exercise

    workout_data.at[idx, 'exercise'] = updated
    save_data(workout_data, 'workout')
    print("Exercise added successfully!")

#Function to log a workout by taking user input for date, category, subcategory, exercise, reps, weight, and duration, then saving the workout log to the CSV file. 
# It includes error handling for invalid input and ensures that the workout log is updated correctly.
def log_workout():
    def prompt(label):
        return input(f"{label}: ").strip()

    df = load_data("workout_log")

    new_row = {
        "date": prompt("Date (YYYY-MM-DD)"),
        "category": prompt("Category"),
        "subcategory": prompt("Subcategory"),
        "exercise": prompt("Exercise"),
        "reps": prompt("Reps"),
        "weight": prompt("Weight"),
        "duration": prompt("Duration (min)")
    }

    df = add_entry(df, new_row)
    save_data(df, "workout_log")
    print("Workout logged!")

# Function to view the user's workout log by loading the workout_log CSV file and displaying each entry in a readable format. 
# It includes error handling for no entries in the workout log.
def view_workout_log():
    workout_log = load_data('workout_log')

    if workout_log.empty:
        print("No workout entries yet. Please log a workout first.")
        return

    print("\nYour workout log:\n")

    for _, row in workout_log.iterrows():
        print(
            f"Date: {row['date']} | "
            f"{row['category']} - {row['subcategory']} | "
            f"Exercise: {row['exercise']} | "
            f"Reps: {row['reps']} | "
            f"Weight: {row['weight']} | "
            f"Duration: {row['duration']} min"
        )

# Function to log water intake by taking user input for date and amount of water consumed, then saving the water log to the CSV file.
#Include error handling for invalid input and ensure that the water log is updated correctly.
def log_water_intake():
    water_log = load_data('water')
    date = input("Please enter the date of your water intake (YYYY-MM-DD): ")
    amount = input("Please enter the amount of water you drank (in ounces): ")
    new_entry = {'date': date, 'amount': amount}
    updated_water_log = add_entry(water_log, new_entry)
    save_data(updated_water_log, 'water')
    print("Water intake logged successfully!")

#Function that allows the user to view their water intake log by loading the water_log CSV file and displaying each entry in a readable format.
def view_water_log():
    water_log = load_data('water')
    if water_log.empty:
        print("No water intake entries yet. Please log your water intake first.")
        return
    else:
        print("Your water intake log:")
        for i, row in water_log.iterrows():
            print(f"{row['date']}: {row['amount']} ounces")

# Main loop to display the menu and handle user choices for logging weight, viewing progress, getting diet suggestions, adding diets, getting workout suggestions, adding exercises, logging workouts, viewing workout logs, logging water intake, viewing water logs, and exiting the chatbot.
#Calls the appropriate functions based on the user's choice and includes error handling for invalid choices. The loop continues until the user chooses to exit the chatbot.
while True:
    show_menu()
    choice = input("Enter your choice (1-11): ")
    if choice == '1':
        log_weight()
    elif choice == '2':
        view_weight_progress()
    elif choice == '3':
        get_diet_plan()
    elif choice == '4':
        add_diet_plan()
    elif choice == '5':
        get_workout_suggestions()
    elif choice == '6':
        add_exercise()
    elif choice == '7':
        log_workout()
    elif choice == '8':
        view_workout_log()
    elif choice == '9':
        log_water_intake()
    elif choice == '10':
        view_water_log()
    elif choice == '11':
        print("Thank you for using the Health & Fitness Chatbot. Make sure to keep working towards your goals! Until next time, stay healthy and fit!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 11.")