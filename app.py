import tkinter as tk
import requests
import threading
import time


server_url = "https://api.thingspeak.com"


class ThresholdApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Threshold Monitoring App")

        tk.Label(root, text="Temperature Threshold:").grid(row=0, column=0, padx=10, pady=10)
        self.temp_threshold = tk.Entry(root)
        self.temp_threshold.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(root, text="Humidity Threshold:").grid(row=1, column=0, padx=10, pady=10)
        self.humid_threshold = tk.Entry(root)
        self.humid_threshold.grid(row=1, column=1, padx=10, pady=10)

        self.send_button = tk.Button(root, text="Set Thresholds", command=self.send_thresholds)
        self.send_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        self.temp_display = tk.Label(root, text="Current Temperature: -")
        self.temp_display.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.humid_display = tk.Label(root, text="Current Humidity: -")
        self.humid_display.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.update_data_thread = threading.Thread(target=self.update_data)
        self.update_data_thread.daemon = True
        self.update_data_thread.start()

    def send_thresholds(self):
        temp_thresh = self.temp_threshold.get()
        humid_thresh = self.humid_threshold.get()
        try:
            request_string = f"{server_url}/update?api_key=UULXX7OEH50YBQ1Y&field3={temp_thresh}&field4={humid_thresh}"
            print(f"Sending {request_string}")
            response = requests.get(request_string)
            if response.status_code == 200:
                print("Thresholds set successfully")
            else:
                print(f"Failed to set thresholds. Status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error: {e}")

    def update_data(self):
        while True:
            try:
                field_1_request_string = f"{server_url}/channels/2711831/fields/1.json?api_key=O0QM4ZXS290A7SUM&results=1"
                response = requests.get(field_1_request_string)
                if response.status_code == 200:
                    data = response.json()
                    feeds = data.get('feeds')
                    temperature = feeds[0].get('field1', "N/A")
                    self.temp_display.config(text="Cannot get temperature from Thingspeak server" if temperature is None
                                             else f"Current Temperature: {temperature}°C")
                else:
                    self.temp_display.config(text="Cannot get temperature from Thingspeak server")
                    print(f"Failed to retrieve data. Status code: {response.status_code}")

                field_2_request_string = f"{server_url}/channels/2711831/fields/2.json?api_key=O0QM4ZXS290A7SUM&results=1"
                response = requests.get(field_2_request_string)
                if response.status_code == 200:
                    data = response.json()
                    feeds = data.get('feeds')
                    humid = feeds[0].get('field2', "N/A")
                    self.humid_display.config(text="Cannot get humid from Thingspeak server" if humid is None
                                            else f"Current Temperature: {humid}°C")
                else:
                    self.humid_display.config(text="Cannot get humid from Thingspeak server")
                    print(f"Failed to retrieve data. Status code: {response.status_code}")
            except requests.RequestException as e:
                print(f"Error: {e}")

            time.sleep(5)


# Set up and run the Tkinter app
root = tk.Tk()
app = ThresholdApp(root)
root.mainloop()