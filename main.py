import tkinter as tk
from tkinter import filedialog
import dataPREprocess
import isolation_ai_BETA
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#function to handle file selection and load data
def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        global data, scaled_features
        data, scaled_features = dataPREprocess.load_and_preprocess_data(file_path)
        anomalies = isolation_ai_BETA.detect_anomalies(scaled_features)
        display_results(data, anomalies)
        plot_data(data)  #embed the plot in the interface

#function to display results in the GUI
def display_results(data, anomalies):
    data['anomaly'] = anomalies
    text_area.config(state=tk.NORMAL)  #allow updates
    text_area.delete(1.0, tk.END)

    anomaly_count = {}
    for index, row in data.iterrows():
        if row['anomaly'] == -1:
            text_area.insert(tk.END, f"Anomaly Detected: User {row['user_id']} at {row['timestamp']}\n")
            anomaly_count[row['user_id']] = anomaly_count.get(row['user_id'], 0) + 1

    text_area.config(state=tk.DISABLED)  #make the text area read-only
    track_users(anomaly_count)

#function to plot data within the GUI
def plot_data(data):
    fig, ax = plt.subplots(figsize=(8, 4))
    normal_data = data[data['anomaly'] == 1]
    anomaly_data = data[data['anomaly'] == -1]

    ax.scatter(normal_data['login_hour'], normal_data['action_duration'], color='blue', label='Normal')
    ax.scatter(anomaly_data['login_hour'], anomaly_data['action_duration'], color='red', label='Anomalies')

    ax.set_title('User Activity and Anomalies')
    ax.set_xlabel('Login Hour')
    ax.set_ylabel('Action Duration')
    ax.legend()

    #embed the plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

#function tot rack users anomaly count
def track_users(anomaly_count):
    suspicious_text.config(state=tk.NORMAL)  #allow updates
    suspicious_text.delete(1.0, tk.END)

    #add title for repeat suspicious users
    suspicious_text.insert(tk.END, "Repeat Anomalies:\n", "title")

    suspicious_users = [user for user, count in anomaly_count.items() if count >= 3]  # Threshold set to 3

    if suspicious_users:
        for user in suspicious_users:
            #insert username in bold and red
            suspicious_text.insert(tk.END, f"User {user} - {anomaly_count[user]} anomalies detected\n", "bold_red")
    else:
        suspicious_text.insert(tk.END, "No users flagged for audit.\n")

    suspicious_text.config(state=tk.DISABLED)  #make text area read only

#GUI window intialization
root = tk.Tk()
root.title("Anomaly Detection Tool")

#load data button
load_button = tk.Button(root, text="Load Data", command=load_file)
load_button.pack(pady=10)

#makes anomaly list scrollable
anomaly_frame = tk.Frame(root)
anomaly_frame.pack(pady=10)

anomaly_scrollbar = tk.Scrollbar(anomaly_frame)
anomaly_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

text_area = tk.Text(anomaly_frame, height=10, width=70, yscrollcommand=anomaly_scrollbar.set)
text_area.pack(side=tk.LEFT)
anomaly_scrollbar.config(command=text_area.yview)
text_area.config(state=tk.DISABLED)  #removes edit feature on the text area

#frame for the plot 
plot_frame = tk.Frame(root)
plot_frame.pack(pady=10)

#makes user list scrollable
suspicious_frame = tk.Frame(root)
suspicious_frame.pack(pady=10)

suspicious_scrollbar = tk.Scrollbar(suspicious_frame)
suspicious_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

suspicious_text = tk.Text(suspicious_frame, height=5, width=70, yscrollcommand=suspicious_scrollbar.set)
suspicious_text.pack(side=tk.LEFT)
suspicious_scrollbar.config(command=suspicious_text.yview)
suspicious_text.config(state=tk.DISABLED)

#makes text tags bold and red for problem users
suspicious_text.tag_configure("title", font=("Helvetica", 12, "bold"))
suspicious_text.tag_configure("bold_red", foreground="red", font=("Helvetica", 10, "bold"))

#start the GUI
root.mainloop()
