#Netflix Analyzer

import pandas as pd
import tkinter
from tkinter import filedialog
import customtkinter
from tkinter import font


#Set CTK Window
customtkinter.set_appearance_mode("System")
app = customtkinter.CTk()
app.geometry("800x400")
app.title("Netflix-Analyzer")
app.grid_columnconfigure(0, weight=1)

#Define Functions

#Get CSV
def filepath():
    global csv
    csv = filedialog.askopenfile()

#Calculate Sum of watched Netlix Shows
def netflixsum():
    global output_text, csv
    df = pd.read_csv(csv)

    df= df.drop(["Profile Name", "Attributes", "Supplemental Video Type", "Device Type", "Bookmark", "Latest Bookmark", "Country"], axis=1)
    df["Start Time"] = pd.to_datetime(df["Start Time"], utc=True)

    df = df.set_index("Start Time")
    df.index = df.index.tz_convert("Europe/Berlin")
    df = df.reset_index()

    df["Duration"] = pd.to_timedelta(df["Duration"])

    shows = df[df["Title"].str.contains("", regex=False)]
    shows = shows[(shows["Duration"] > "0 days 00:01:00")]

    sum_duration = shows["Duration"].sum()
    output_text.insert(customtkinter.END, str(sum_duration))
    
  
#Define Buttons/Labels
label_font = customtkinter.CTkFont(family="Helvetica", size=22, weight="bold")
button_font = customtkinter.CTkFont(family="Helvetica", size=18)
text_font = customtkinter.CTkFont(family="Helvetica", size=18)


label = customtkinter.CTkLabel(app, text="Calculate the Sum of your watched Netflix Shows/Movies", fg_color="transparent", font=label_font)
label.grid(row=0, column=0, padx=20, pady=20)

csv_button = customtkinter.CTkButton(app, text="Select your Viewing Activity.csv File", command=filepath, font=button_font)
csv_button.grid(row=1, column=0, padx=20, pady=20)

sum_button = customtkinter.CTkButton(app, text="Calculate Sum of watched Netflix Shows", command=netflixsum, font=button_font)
sum_button.grid(row=2, column=0, padx=20, pady=20)

output_text = customtkinter.CTkTextbox(app, height=5, width=160, font=text_font)
output_text.grid(row=3, column=0, padx=20, pady=30)

app.mainloop()
