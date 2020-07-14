import requests
import bs4
import tkinter as tk
import plyer
import time
import datetime
import threading


# get html data of website
def get_html_data(url):
    data = requests.get(url)
    return data


# parsing html and extracting data
def get_corona_detail_of_india():
    url = "https://www.mohfw.gov.in/"
    html_data = get_html_data(url)
    bs = bs4.BeautifulSoup(html_data.text, 'html.parser')
    info_div = bs.find("div", class_="information_row").find_all("div", class_="iblock")
    all_details = ""
    for block in info_div:
        count = block.find("span", class_="icount").get_text()
        text = block.find("div", class_="info_label").get_text()
        all_details = all_details + text + " : " + count + "\n"
    return all_details


# function use to  reload the data from website
def refresh():
    newdata = get_corona_detail_of_india()
    print("Refreshing..")
    mainLabel['text'] = newdata


# function for notifying...
def notify_me():
    while True:
        plyer.notification.notify(
            title="COVID 19 cases of INDIA",
            message=get_corona_detail_of_india(),
            timeout=10,
            app_icon='icon.ico'
        )
        time.sleep(30)


# creating gui:
root = tk.Tk()
root.geometry("900x800")
root.iconbitmap("icon.ico")
root.title("CORONA DATA TRACKER - INDIA")
root.configure(background='white')
f = ("poppins", 25, "bold")
banner = tk.PhotoImage(file="banner.png")
bannerLabel = tk.Label(root, image=banner)
bannerLabel.pack()
mainLabel = tk.Label(root, text=get_corona_detail_of_india(), font=f, bg='white')
mainLabel.pack()

reBtn = tk.Button(root, text="REFRESH", font=f, relief='solid', command=refresh)
reBtn.pack()

# create a new thread
th1 = threading.Thread(target=notify_me)
th1.setDaemon(True)
th1.start()

