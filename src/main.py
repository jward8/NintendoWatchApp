from time import sleep
from selenium import webdriver
from twilio.rest import Client


class nintendoWatch:
    def __init__(self):
        self.driver = webdriver.Chrome('C:\\Users\\JackMichael\\Documents\\Coding\\NintendoWatchApp\\src\\chromedriver')
        sleep(2)

        # self.zipBtn = self.driver.find_element_by_id("storeId-utilityNavBtn")
        # self.zipBtn.click()
        # sleep(5)
        #
        # # input madison area code and submit
        # self.zipInput = self.driver.find_element_by_id("zipOrCityState")\
        #     .send_keys("53715")
        # self.lookBtn = self.driver.find_element_by_xpath("//button[@data-test='storeLocationSearch-button']")\
        #     .click()
        #
        # sleep(4)
        #
        # #select Madison East as store
        # self.storeBtn = self.driver.find_element_by_xpath("//div[@data-test='storeIdSearch-item-2106']/button")\
        #     .click()


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


def bestBuy(self):
    self.driver.get(
        "https://www.bestbuy.com/site/nintendo-switch-32gb-console-neon-red-neon-blue-joy-con/6364255.p?skuId=6364255")
    best_btn = self.driver.find_element_by_xpath("//div[@class='fulfillment-add-to-cart-button']/div/button")
    store_pickup = self.driver.find_element_by_xpath("//*[@id='fulfillment-fulfillment-summary-4c1e0ec7-88db-44f0-b3c8-9940cd592454']/div/div/div/div/div[2]/div/span")

    if best_btn.text == 'Sold Out' or "unavailable" in store_pickup.text:
        send_msg("Sold out at Best Buy")
    else:
        send_msg("In Stock! Buy Soon!")


checker = nintendoWatch()
bestBuy(checker)
