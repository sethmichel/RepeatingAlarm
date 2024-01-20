import tkinter as tk
import time
from threading import Thread

class AlarmApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Repeating Alarm App")
        self.master.geometry("400x200")
        self.master.configure(bg='#f0f0f0')  # Set background color

        self.minutes = tk.StringVar()
        self.seconds = tk.StringVar()

        self.label = tk.Label(master, text="Enter the time:", bg='#f0f0f0', font=('Helvetica', 14))
        self.label.pack(pady=10)

        # Frame for minutes input
        minutes_frame = tk.Frame(master, bg='#f0f0f0')
        minutes_frame.pack(side=tk.TOP)
        self.label_minutes = tk.Label(minutes_frame, text="Minutes:", bg='#f0f0f0', font=('Helvetica', 12), anchor="e")
        self.label_minutes.pack(side=tk.LEFT, padx=5)
        self.entry_minutes = tk.Entry(minutes_frame, textvariable=self.minutes, width=5, font=('Helvetica', 12))
        self.entry_minutes.pack(side=tk.LEFT)

        # Frame for seconds input
        seconds_frame = tk.Frame(master, bg='#f0f0f0')
        seconds_frame.pack(side=tk.TOP)
        self.label_seconds = tk.Label(seconds_frame, text="Seconds:", bg='#f0f0f0', font=('Helvetica', 12), anchor="e")
        self.label_seconds.pack(side=tk.LEFT, padx=5)
        self.entry_seconds = tk.Entry(seconds_frame, textvariable=self.seconds, width=5, font=('Helvetica', 12))
        self.entry_seconds.pack(side=tk.LEFT)

        # Set Alarm and Cancel Alarm buttons
        set_cancel_frame = tk.Frame(master, bg='#f0f0f0')
        set_cancel_frame.pack(side=tk.TOP, pady=10)
        self.set_button = tk.Button(set_cancel_frame, text="Set Alarm", command=self.set_alarm, bg='#4CAF50', fg='white', font=('Helvetica', 12))
        self.set_button.pack(side=tk.LEFT, padx=5)
        self.cancel_button = tk.Button(set_cancel_frame, text="Cancel Alarm", command=self.cancel_alarm, bg='#F44336', fg='white', font=('Helvetica', 12))
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        # Pause Alarm and Continue Alarm buttons
        pause_continue_frame = tk.Frame(master, bg='#f0f0f0')
        pause_continue_frame.pack(side=tk.TOP)
        self.pause_button = tk.Button(pause_continue_frame, text="Pause Alarm", command=self.pause_alarm, bg='#808080', fg='white', font=('Helvetica', 12))
        self.pause_button.pack(side=tk.LEFT, padx=5)
        self.continue_button = tk.Button(pause_continue_frame, text="Continue Alarm", command=self.continue_alarm, bg='#2196F3', fg='white', font=('Helvetica', 12))
        self.continue_button.pack(side=tk.LEFT, padx=5)

        self.alarm_thread = None
        self.remaining_time = 0
        self.paused = False
        self.stop_thread = False

    def set_alarm(self):
        if self.alarm_thread and self.alarm_thread.is_alive():
            self.cancel_alarm()  # Cancel the current alarm

        try:
            minutes = int(self.minutes.get())
            seconds = int(self.seconds.get())
            total_seconds = minutes * 60 + seconds

            self.label.config(text=f"Counting down: {minutes} minutes {seconds} seconds")
            self.master.update()

            self.alarm_thread = Thread(target=self.countdown, args=(total_seconds,))
            self.alarm_thread.start()

        except ValueError:
            self.label.config(text="Please enter valid minutes and seconds.")

    def countdown(self, seconds):
        self.remaining_time = seconds
        while self.remaining_time > 0 and not self.paused and not self.stop_thread:
            minutes, sec = divmod(self.remaining_time, 60)
            self.label.config(text=f"Counting down: {minutes} minutes {sec} seconds")
            self.master.update()
            time.sleep(1)
            self.remaining_time -= 1

        if not self.paused and not self.stop_thread:
            self.label.config(text="Time's up!")
            self.master.update()
            self.repeat_alarm()

    def repeat_alarm(self):
        # Automatically repeat the alarm after a delay (e.g., 3 seconds)
        repeat_delay = 3
        self.master.after(repeat_delay * 1000, self.set_alarm)

    def pause_alarm(self):
        self.paused = True
        self.label.config(text="Alarm paused")
        self.master.update()

    def continue_alarm(self):
        self.paused = False
        self.label.config(text="Resuming alarm...")
        self.master.update()
        self.set_alarm_with_remaining_time()

    def set_alarm_with_remaining_time(self):
        # Set a new alarm with the remaining time from when it was paused
        self.alarm_thread = Thread(target=self.countdown, args=(self.remaining_time,))
        self.alarm_thread.start()

    def cancel_alarm(self):
        self.paused = False
        self.remaining_time = 0  # Reset remaining_time
        self.stop_thread = True  # Set the flag to stop the alarm thread
        if self.alarm_thread and self.alarm_thread.is_alive():
            self.alarm_thread.join()  # Stop the current alarm thread
        self.label.config(text="Alarm canceled")
        self.master.update()
        self.stop_thread = False  # Reset the flag for future alarms

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmApp(root)
    root.mainloop()
