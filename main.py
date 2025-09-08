import requests
from tkinter import *
from tkinter import filedialog, simpledialog, messagebox
import datetime
import smtplib
import os

WINDOW_BG = "#0D1B2A"
CANVAS_BG = "#1B263B"
my_email = os.environ.get("FROM_MAIL")      # <--SET YOU EMAIL
password = os.environ.get("APP_PASSWORD")   # <--SET YOU EMAIL APP PASSWORD

CRYPTO_ENDPOINT = "https://min-api.cryptocompare.com/data/top/totalvolfull"

crypto_params = {
    "limit": 10,
    "tsym": "USD",
}

today = datetime.datetime.now()
month = today.strftime("%b")
day = today.strftime("%d")
hour = today.strftime("%H")
minute = today.strftime("%M")
am = today.strftime("%p")
full_time = f"{month} {day}, {hour}:{minute}{am}"
# print(full_time)
# print(today)

response = requests.get(CRYPTO_ENDPOINT, params=crypto_params)
cp_data = response.json()["Data"]
coins = []

data_list = [value for value in cp_data]
for coin in data_list:
    name = coin['CoinInfo']['FullName']
    symbol = coin['CoinInfo']['Name']
    if "RAW" in coin and "USD" in coin["RAW"]:
        price = coin["RAW"]["USD"].get("PRICE", "N/A")
        change = coin["RAW"]["USD"].get("CHANGEPCT24HOUR", "N/A")
        # print(name, price, change)
#    price = coin["RAW"]["USD"]["TYPE"]
#    price_change = coin["DISPLAY"]["USD"]["CHANGEPCT24HOUR"]
#    print(coin)
    coins.append((name, change))

sorted_coins = sorted(coins, key=lambda x: x[1])
top_gainers = sorted_coins[-5:]
top_losers = sorted_coins[:5]

gainers = [coin for coin in top_gainers if coin[1] > 0]
losers = [coin for coin in top_losers if coin[1] < 0]

gainers_sorted = sorted(gainers, key=lambda x: x[1], reverse=True)
losers_sorted = sorted(losers, key=lambda x: x[1])

# print("Top Gainers:")
# for coin, pct in gainers_sorted:
#     gainers = f"{coin}: {round(pct, 2)}%"
#     print(gainers)
#
# print("\nTop Losers:")
# for coin, pct in losers_sorted:
#     print(f"{coin}: {round(pct, 2)}%")

def save_to_txt():
    content = f"Data for {full_time}\n\nTop Gainers:\n"
    for coin, pct in gainers_sorted:
        content += f"{coin}: {round(pct, 2):.2f}%\n"

    content += "\nTop Losers:\n"
    for coin, pct in losers_sorted:
        content += f"{coin}: {round(pct, 2):.2f}%\n"

    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    if file_path:
        with open(file_path, "w") as f:
            f.write(content)


gain_content = f"Data for {full_time}\n\nTop Gainers:\n"
for coin, pct in gainers_sorted:
    gain_content += f"{coin}: {round(pct, 2):.2f}%\n"
gain_content += "\nTop Losers:\n"
for coin, pct in losers_sorted:
    gain_content += f"{coin}: {round(pct, 2):.2f}%\n"


def send_mail():
    to_email = simpledialog.askstring("Input", "Enter your email")
    try:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
    
            connection.sendmail(from_addr=my_email,
                                to_addrs=to_email,
                                msg=f"Subject:Crypto Market Data\n\n{gain_content}"
                                )
        messagebox.showinfo(message="Email Sent")
    except Exception as e:
        messagebox.showinfo(message=f"Error sending email: {e}")


window = Tk()
window.title("Crypto Data")
window.minsize(height=500, width=400)
window.config(bg=WINDOW_BG,padx=50, pady=20)

header_label = Label(text=f"Top Gainers for {full_time}",anchor="w", font=("Ariel", 20, "bold"))

header_label.config(fg="white", bg=WINDOW_BG)
header_label.grid(column=1, row=0)

canvas1 = Canvas(width=400, height=150)
canvas1.config(bg=CANVAS_BG, highlightthickness=0)
y = 30
for coin, pct in gainers_sorted:
    fill_color = "#00B894" if pct > 0 else "#E17055"
    canvas1.create_text(
        50, y,
        anchor="w",
        width=270,
        text=f"⬆️ {coin:<27} {pct:>6.2f}%",
        fill=fill_color,
        font=("Arial", 18, "italic")
    )
    y += 25

# word_text = canvas1.create_text(400,263, text="", fill="black",font=("Ariel", 60, "bold"))
canvas1.grid(row=1, column=0,columnspan=2, pady=20)

losers_txt = Label(text="Losers:",anchor="w", font=("Ariel", 20, "bold"))
losers_txt.config(fg="white", bg=WINDOW_BG)
losers_txt.grid(row=2, column=0, columnspan=2)

canvas2 = Canvas(width=400, height=100)
canvas2.config(bg=CANVAS_BG, highlightthickness=0)
y = 30
for coin, pct in losers_sorted:
    fill_color = "#00B894" if pct > 0 else "#E17055"
    canvas2.create_text(
        50, y,
        anchor="w",
        width=300,
        text=f"⬇️️{coin:<27} {pct:>6.2f}%",
        fill=fill_color,
        font=("Arial", 18, "italic")
    )
    y += 25

# word_text = canvas1.create_text(400,263, text="", fill="black",font=("Ariel", 60, "bold"))
canvas2.grid(row=3, column=0,columnspan=2,pady=20)

download_btn = Button(text="Download")
download_btn.config(highlightthickness=0, highlightbackground=WINDOW_BG, command=save_to_txt)
download_btn.grid(row=4, column=1, pady=20)

email_btn = Button(text="Send to mail")
email_btn.config(highlightthickness=0, highlightbackground=WINDOW_BG, command=send_mail)
email_btn.grid(row=5, column=1)


window.mainloop()
