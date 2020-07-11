from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from twilio.rest import Client


class nintendoWatch:
    def __init__(self):
        self.driver = webdriver.Chrome('C:\\Users\\JackMichael\\Documents\\Coding\\NintendoWatchApp\\src\\chromedriver')
        sleep(2)


def send_msg(message,stores, place):
    account_sid = 'ACf46189a9ceca2b697f802f912661f127'
    auth_token = 'd294e42e19c2fedc65a006946efe8fa7'
    client = Client(account_sid, auth_token)
    store_msg = place + ", " + message + "\n"

    if len(stores) != 0:
        for x in stores:
            store_msg += x['store_name'] + ": " + x['miles'] + "\n"

    message = client.messages \
        .create(
        body=store_msg,
        from_='+12029521329',
        to='+14147952004'
    )


def check_bestBuy(self):
    self.driver.get(
        "https://www.bestbuy.com/site/nintendo-switch-32gb-console-neon-red-neon-blue-joy-con/6364255.p?skuId=6364255")
    best_btn = self.driver.find_element_by_xpath("//div[@class='fulfillment-add-to-cart-button']/div/button")
    store_pickup = self.driver.find_element_by_xpath("//*[@id='fulfillment-fulfillment-summary-4c1e0ec7-88db-44f0-b3c8-9940cd592454']/div/div/div/div/div[2]/div/span")

    if best_btn.text == 'Sold Out' or "unavailable" in store_pickup.text:
        send_msg("Sold out at Best Buy")
    else:
        send_msg("In Stock! Buy Soon!")


def check_target(self):
    ret_list = []
    self.driver.get("https://www.target.com/p/nintendo-switch-with-neon-blue-and-neon-red-joy-con/-/A-77464001")
    sleep(3)
    self.driver.find_element_by_xpath("//button[@data-test='fiatsButton']")\
        .click()
    sleep(1)
    self.driver.find_element_by_xpath("//a[@class='Link-sc-1khjl8b-0 bTKAgl']")\
        .click()
    sleep(2)

    #sets the location
    self.driver.find_element_by_xpath("//input[@id='storeSearch']").click()
    self.driver.find_element_by_xpath("//input[@id='storeSearch']").send_keys(Keys.CONTROL + "a")
    self.driver.find_element_by_xpath("//input[@id='storeSearch']").send_keys("53715")

    self.driver.find_element_by_xpath("//button[@data-test='fiatsUpdateLocationSubmitButton']")\
        .click()
    sleep(1)
    self.driver.find_element_by_class_name('switch-track')\
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
            ret_list.append(entry)

    if len(ret_list) > 0:
        send_msg("In Stock at these locations", ret_list, "Target")
    else:
        send_msg("Sold out at Target, closest store is not within 20 miles", [], "Target")

    # if int(text[1]) > 20:
    #     send_msg("Sold out at Target, closest store is " + text[2] + " miles away", [])
    # else:
    #     for loc in locations:
    #         text = loc.text.split()
    #         if
    #     send_msg("In Stock! A store in 20 miles has one")



checker = nintendoWatch()
check_target(checker)
