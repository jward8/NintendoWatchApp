from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from twilio.rest import Client


class nintendoWatch:
    def __init__(self):
        self.driver = webdriver.Chrome('C:\\Users\\JackMichael\\Documents\\Coding\\NintendoWatchApp\\src\\chromedriver')
        sleep(2)


def send_msg(message):
    account_sid = 'ACf46189a9ceca2b697f802f912661f127'
    auth_token = 'd294e42e19c2fedc65a006946efe8fa7'
    client = Client(account_sid, auth_token)

    message = client.messages \
        .create(
        body=message,
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
    first_location = self.driver.find_element_by_xpath("//div[@data-test='storeAvailabilityStoreCard']/div/h3/span[2]")
    text = first_location.text.split()

    if int(text[0]) > 20:
        send_msg("Sold out at Target")
    else:
        send_msg("In Stock! A store in 20 miles has one")



checker = nintendoWatch()
check_target(checker)
