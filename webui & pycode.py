import customtkinter as ctk
import tkinter
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import openpyxl as opxl
from datetime import date

# Entry Web UI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.geometry("990x540")

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

title = ctk.CTkLabel(master=frame, text="UTA Datathon 2023", font=('Roboto', 20))
title.pack(pady=12, padx=10)

label = ctk.CTkLabel(master=frame,text='Google Trends, But Tweets!')
label.pack()

entry = ctk.CTkEntry(master=root, placeholder_text="Enter a word to search for: ", width=180, height=25, border_width=2, corner_radius=10)
entry.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

# Grab and read Excel file
excel_file = 'TwitterHealthData.xlsx'
health_tweets = pd.read_excel(excel_file)

# ID -> Date format function
tid = 1626316977756160000

def get_tweet_timestamp(tid):
    offset = 1288834974657
    tstamp = (tid >> 22) + offset
    utcdttime = date.fromtimestamp(tstamp/1000)
    return utcdttime

def create_graph():
  # Grab word from entered text in entry variable defined above^ and lower case it
  word = entry.get().lower()
  # Filter; lower case the database and search for it
  health_tweets['tweet_text'] = health_tweets['tweet_text'].str.lower()
  health_tweets_word = health_tweets[health_tweets['tweet_text'].str.contains(word)]
  # Divide into pandas columns the full date, year, and month
  tweet_date_word = []
  tweet_year_word = []
  tweet_month_word = []
  for id in health_tweets_word['tweet_id']:
    tweet_date_word.append(str(get_tweet_timestamp(id)).split('-'))
  for e in tweet_date_word:
    tweet_year_word.append(e[0])
    tweet_month_word.append(e[1])
  word_tweets = pd.DataFrame({'tweet_id': health_tweets_word['tweet_id'], 'tweet_text': health_tweets_word['tweet_text'], 'tweet_date': tweet_date_word, 'tweet_year': tweet_year_word, 'tweet_month': tweet_month_word})
  # Get min and max year values and their respective counts in list counter = [[Year, Count], [Year1, Count1], ...]]
  min = word_tweets['tweet_year'].min()
  max = word_tweets['tweet_year'].max()
  counter = []
  listrange = list(range(int(min), int(max) + 1))
  for e in listrange:
    counter.append(word_tweets.loc[word_tweets['tweet_year'] == str(e)].shape[0])
  categorized_years = list(zip(counter, listrange))
  print(categorized_years)
  # Graphing; matplotlib
  counter_sum = sum(counter)
  x = counter
  y = listrange
  plt.style.use('seaborn')
  plt.clf()
  plt.bar(y, x, 0.5, bottom=None, color='grey', edgecolor='blue')
  plt.title('Tweets with the word: ' + word + ' (total: ' + str(counter_sum) + ' tweets)', pad=15, font='Calibri', size=15)
  plt.xlabel('Year', font='Calibri', size=15)
  plt.ylabel('Number of tweets', rotation=90, ha='center', font='Calibri', size=15)
  plt.xticks(y, rotation=45, font='Calibri', size=15)
  count = 0
  for i in listrange:
    plt.text(i, x[count], x[count], ha='center', va='bottom', color='blue', font='Calibri', size=15)
    count += 1
  plt.show()
  print(counter_sum)

# Search button in UI; when button clicked, new graph is made in same UI window
button = ctk.CTkButton(master=frame, width = 70, text="Search", corner_radius=10, command=lambda: create_graph())
button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

root.mainloop()