import pandas as pd
import numpy as np
import logging
import random
import string
import matplotlib.pyplot as plt

def generate_log_entry():
    """
    generate a random log with timestamp ,loglevel,action and user
    """
    timestamp = pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
    loglevel = random.choice(["INFO","DEBUG","ERROR","WARNING"])
    action = random.choice(["Login","Logout","Data Request","File Upload","Download","Error"])
    user = ''.join(random.choices(string.ascii_uppercase + string.digits ,k=6))    #The length of the user will be 6
    return f" {timestamp} - {loglevel} - {action} - User:{user}"

#Function to write logs to a file 
def write_logs_to_file(log_filename,num_entries=100):
    """
    write the specified number of logs in the given file 
    """
    try:
        with open(log_filename , 'w') as file:
            for _ in range(num_entries):
                log=generate_log_entry()
                file.write(log + "\n")
        print(f"Logs have been successfully written to the file {log_filename}.")
    except Exception as e:
        logging.error(f"Error writing logs to file {log_filename}: {e}")
        print(f"An error occured writing to the file.")
    
#Function to read the log file and processed it
def load_and_process_logs(log_filename="generate_logs.txt"):
    """
    load and processes the logs from the given file cleaning and parsing the timestamps
    """
    try:
        #Read the log file into a pandas dataframe,splitting by the ' - ' separator.
        logs = []
        with open(log_filename , 'r') as file:
            for line in file:
                parts =line.strip().split(" - ")
                if len(parts) == 4:
                    timestamp,log_level,action,user = parts
                    user = user.replace("User:", "").strip()
                    logs.append([timestamp ,log_level ,action ,user])

        df = pd.DataFrame(logs ,columns=["Timestamp","Log level","Action","Users"])

        #Clean and trim spaces around the timestamp
        #df['Timestamp'] = df['Timestamp'].str.strip()

        #Convert the timestamp column to dataframe
        df["Timestamp"] = pd.to_datetime(df["Timestamp"],errors="coerce")

        #Drop rows with invalid timestamp
        df.dropna(subset=["Timestamp"],inplace=True)

        if df.empty:
            print("No valid data found after timestamp conversion")
        else:
            print("Data after timestamp conversion.")
            print(df.head())         #show the data after cleaning
            
        #set the timestamp column as index for time based calculations.
        df.set_index("Timestamp" ,inplace=True)
        return df
    except Exception as e:
        print(f"Error processing log file {e}")
        return None
    
#Function to perform basic statistical analysis using pandas and numpy
def analyze_data(df):
    """
    performs the basic analysis such as counting log levels and actions and computing basic statistics such as max,min and avg etc
    """
    try:
        if df is None or df.empty:
            print("No data to analyze")
            return None
        
        #count the occurrences of each log level
        log_level_counts = df['Log level'].value_counts()

        #Counts the action of each occurences 
        action_counts = df['Action'].value_counts()

        log_counts = len(df)      #Length of the logs
        unique_users = df['Users'].nunique()   #Number of unique users
        logs_per_day = df.resample('D').size()   #Number of logs per day

        #Averages of actions per day
        averages_logs_per_day = logs_per_day.mean()

        #Max logs day
        max_logs_per_day = logs_per_day.max()

        #Display summary statistics
        print(f"Log Level Counts:{log_level_counts}")
        print(f"Counts the actions:{action_counts}")
        print(f"Length of the Logs :{log_counts}")
        print(f"Unique users :{unique_users}")
        print(f"Averages of actions :{averages_logs_per_day:.2f}")
        print(f"Max logs day:{max_logs_per_day}")

        # create a dictionary to returm the analysis results
        stats = {
            "log_level_counts":log_level_counts,
            "action_counts":action_counts,
            "log_counts":log_counts,
            "unique_users":unique_users,
            "averages_logs_per_day":averages_logs_per_day,
            "max_logs_per_day":max_logs_per_day
        }
        return stats
    except Exception as e:
        print(f"Error analyzing data {e}")
        return None
    
#Function to visualize trends over time using matplotlib
def visualize_trends(df):
    """
    visualize log frequency trends over time using matplotlib
    """
    try:
        #Resample data to get the number of logs per day
        logs_per_day = df.resample('D').size()

        #plotting log frequency over time using matplotlib
        plt.figure(figsize=(10,5))
        plt.plot(logs_per_day.index,logs_per_day.values,marker='o',linestyle='-',color='b')

        #customize the plot 
        plt.title("Log freaurncy over time")
        plt.xlabel("Date")
        plt.ylabel("Number of Logs")
        plt.xticks(rotation=45)
        plt.grid(True)

        #show the plot
        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error visualizing trends {e}")
       
if __name__ == "__main__":    
    log_filename = "generated_logs.txt"

    #step1 : write random logs to the file
    write_logs_to_file (log_filename,num_entries=200)

    #step2 : Load and process logs to the file
    df_logs = load_and_process_logs(log_filename)

    #step3 : perform basic analysis on the log data
    if df_logs is not None:
        stats = analyze_data(df_logs)
    #step4 : Visualize trends over time
        visualize_trends(df_logs)