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

    client.messages \
        .create(
        body=message,
        from_='+12029521329',
        to='+16085142318'
    )


def check_bestBuy(self):
    self.driver.get(
        "https://www.bestbuy.com/site/nintendo-switch-32gb-console-neon-red-neon-blue-joy-con/6364255.p?skuId=6364255")
    best_btn = self.driver.find_element_by_xpath("//div[@class='fulfillment-add-to-cart-button']/div/button")

    if best_btn.text == 'Sold Out':
        return False
    else:
        store_pickup = self.driver.find_element_by_xpath(
            "//*[@id='fulfillment-fulfillment-summary-4c1e0ec7-88db-44f0-b3c8-9940cd592454']/div/div/div/div/div[2]/div/span")
        if "unavailable" in store_pickup.text:
            return False
        return True


def check_target(self):
    ret_list = []
    self.driver.get("https://www.target.com/p/nintendo-switch-with-neon-blue-and-neon-red-joy-con/-/A-77464001")
    sleep(3)
    self.driver.find_element_by_xpath("//button[@data-test='fiatsButton']") \
        .click()
    sleep(1)
    self.driver.find_element_by_xpath("//a[@data-test='storeSearchLink']") \
        .click()
    sleep(2)

    # sets the location
    input_location = "//input[@id='storeSearch']"
    self.driver.find_element_by_xpath(input_location).click()
    self.driver.find_element_by_xpath(input_location).send_keys(Keys.CONTROL + "a")
    self.driver.find_element_by_xpath(input_location).send_keys("53715")

    self.driver.find_element_by_xpath("//button[@data-test='fiatsUpdateLocationSubmitButton']") \
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
            ret_list.append(entry)

    return ret_list


def summarize(self):
    at_bestBuy = check_bestBuy(self)
    target_list = check_target(self)
    at_target = len(target_list) > 0

    summary_msg = "Nintendo Switch Locations: \n"
    if at_bestBuy:
        summary_msg += "BestBuy: It's available! Check website! \n"
    else:
        summary_msg += "BestBuy: Unavailable :( \n"

    if at_target:
        summary_msg += "Target: It's available at these locations: \n"
        for x in target_list:
            summary_msg += x['store_name'] + ": " + x['miles'] + "\n"
    else:
        summary_msg += "Target: Unavailable in the nearest 20 miles :("

    send_msg(summary_msg)


checker = nintendoWatch()
summarize(checker)
