# Crypto Tracker GUI

A simple **Python Tkinter application** that displays the **top gainers and losers in the cryptocurrency market**.  
The app provides a clean GUI, allows exporting results to a `.txt` file, and even lets you **send results directly to your email**.  

---

## Features
- Display **Top Gainers** and **Top Losers** (sorted from highest to lowest).
- Clean **Tkinter GUI** with customizable themes.
- Export data to `.txt` file with one click.
- Send results directly to your **email inbox**.
- Percentages are rounded to **1–2 decimal places** for readability.


## 📷 Screenshot
(Add a screenshot of your app here)


## ⚙️ Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/crypto-tracker-gui.git
   cd crypto-tracker-gui
    ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables for secure email sending:

   * On macOS/Linux:

     ```bash
     export FROM_MAIL="your_email@example.com"
     export APP_PASSWORD="your_app_password"
     ```

   * Or simply make the configurations directly in your code:

     ```bash
      my_email = "your_email@example.com"
      password = "your_app_password"
     ```

   >  **Note:** You must generate an **App Password** from your email provider (e.g., Gmail, Outlook) since direct login with regular passwords is often blocked.

4. Run the app:

   ```bash
   python main.py
   ```


## Future Improvements

* Add support for multiple timeframes (24h, 7d, 30d).
* Integrate live refresh for **real-time updates**.
* Allow multiple email recipients.
