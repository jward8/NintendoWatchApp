from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from twilio.rest import Client
import tkinter as tk
from tkinter import Text
import os

class nintendoWatch:
    def __init__(self):
        chrome_options = Options()  
        chrome_options.add_argument("--headless")
        chrome_options.binary_location = 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
        self.driver = webdriver.Chrome(executable_path='C:\\Users\\JackMichael\\Documents\\Coding\\NintendoWatchApp\\src\\chromedriver',
        options=chrome_options)
        sleep(2)


def send_msg(message):
    account_sid = 'ACf46189a9ceca2b697f802f912661f127'
    auth_token = 'd294e42e19c2fedc65a006946efe8fa7'
    client = Client(account_sid, auth_token)

    client.messages \
        .create(
        body=message,
        from_='+12029521329',
        to='+14147952004'
    )


def check_bestBuy(self,switch_best):

    for x in range(2):
        self.driver.get(switch_best['url'][x])
        best_btn = self.driver.find_element_by_xpath("//div[@class='fulfillment-add-to-cart-button']/div/button")

        if best_btn.text == 'Sold Out':
            continue
        else:
            store_pickup = self.driver.find_element_by_xpath(
                "//*[@id='fulfillment-fulfillment-summary-4c1e0ec7-88db-44f0-b3c8-9940cd592454']/div/div/div/div/div[2]/div/span")
            if "unavailable" in store_pickup.text:
                continue
            switch_best['availability'][x] = True
    return switch_best


def check_target(self, switch_target):

    for x in range(2):
        self.driver.get(switch_target["url"][x])
        sleep(3)
        switch_location = self.driver.find_element_by_xpath("//button[@data-test='fiatsButton']")
        self.driver.execute_script("arguments[0].click()", switch_location)
        sleep(1)
        self.driver.find_element_by_xpath("//a[@data-test='storeSearchLink']") \
            .click()
        sleep(2)

        # sets the location
        input_location = "//input[@id='storeSearch']"
        self.driver.find_element_by_xpath(input_location).click()
        self.driver.find_element_by_xpath(input_location).send_keys(Keys.CONTROL + "a")
        self.driver.find_element_by_xpath(input_location).send_keys("53715")

        self.driver.find_element_by_xpath("//button[@data-test='fiatsUpdateLocationSubmitButton']")\
            .click()
        sleep(1)
        self.driver.find_element_by_class_name('switch-track') \
            .click()
        sleep(1)
        locations = self.driver.find_elements_by_xpath("//div[@data-test='storeAvailabilityStoreCard']")

        for loc in locations:
            text = str.splitlines(loc.text)
            if int(text[1].split()[0]) < 20:
                entry = {
                    'store_name': text[0],
                    'miles': text[1]
                }
                switch_target['locations'][x].append(entry)

    return switch_target


def summarize(self):
    switch_avail = [
        {
            "store": "Target",
            "url": ["https://www.target.com/p/nintendo-switch-with-neon-blue-and-neon-red-joy-con/-/A-77464001",
                    "https://www.target.com/p/nintendo-switch-with-gray-joy-con/-/A-77464002"],
            "locations": [[],[]],
            "availability": [False,False]
        },
        {
            "store": "Best Buy",
            "url": ["https://www.bestbuy.com/site/nintendo-switch-32gb-console-neon-red-neon-blue-joy-con/6364255.p?skuId=6364255",
                    "https://www.bestbuy.com/site/nintendo-switch-32gb-console-gray-joy-con/6364253.p?skuId=6364253"],
            "locations": [[],[]],
            "availability": [False,False]
        }
    ]
    switch_avail[1] = check_bestBuy(self, switch_avail[1])
    switch_avail[0] = check_target(self,switch_avail[0])
    summary_msg = "Nintendo Switch Locations: \n"

    for x in switch_avail:
        if x['availability'][0] or x['availability'][1]:
            if x['availability'][0] and x['availability'][1]:
                summary_msg += x['store'] + " either of both colors at these locations:\n"
                for y in range(2):
                    for loc in x['locations'][y]:
                        summary_msg += loc['store_name'] + ": " + loc['miles'] + "\n"
            elif x['availability'][0]:
                summary_msg += x['store'] + " has the red and blue switch at these locations:\n"
                for loc in x['locations'][0]:
                    summary_msg += loc['store_name'] + ": " + loc['miles'] + "\n"
            elif x['availability'][1]:
                summary_msg += x['store'] + " has the grey switch at these locations:\n"
                for loc in x['locations'][1]:
                    summary_msg += loc['store_name'] + ": " + loc['miles'] + "\n"
        else:
            summary_msg += x['store'] + " doesn't have any switches :(\n"

    send_msg(summary_msg)


def setup_gui():
    root = tk.Tk()
    canvas = tk.Canvas(root, height=400, width=800, bg="#ffffff")
    canvas.pack()

    canvas.create_text(400,50,text="Nintendo Switch Watcher", font=("Helvetica",24,"bold"))

    left_frame = tk.Frame(root, bg="#00c3e3")
    left_frame.place(relwidth=.2,relheight=1)

    right_frame = tk.Frame(root, bg='#ff4554')
    right_frame.place(relwidth=.2,relheight=1,relx=.8)

    run_app = tk.Button(root, text="Run Notifier", padx=10, pady=5, fg="white", bg='#00c3e3', 
        command=start_up)
    run_app.pack()

    add_notifee = tk.Button(root, text="Add Notifiee", padx=10, pady=5,fg='white', bg='#ff4554')
    add_notifee.pack()

    root.mainloop()

def start_up():
    checker = nintendoWatch()
    summarize(checker)

if __name__ == '__main__':
    setup_gui()
