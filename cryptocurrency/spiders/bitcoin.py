import scrapy
from cryptocurrency.items import CryptocurrencyItem
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logzero import logfile, logger
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import json
import loguru
from lxml import etree


BROWSER_EXE = 'C:\Program Files\Mozilla Firefox/firefox.exe'
GECKODRIVER = 'D:\geckodriver.exe'
FIREFOX_BINARY = FirefoxBinary(BROWSER_EXE)

class BitcoinSpider(scrapy.Spider):
    name = 'bitcoin'
    allowed_domains = ['coinmarketcap.com/currencies/bitcoin/historical-data/']
    start_urls = ['https://coinmarketcap.com/currencies/bitcoin/historical-data/']
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            "cryptocurrency.middlewares.RotateProxyMiddleware": 300, #Unhealthy proxy give timeout exception sometimes
            "cryptocurrency.middlewares.RotateAgentMiddleware": 301,
            "cryptocurrency.middlewares.CryptocurrencyMiddleware": 302
        },
        "ITEM_PIPELINES": {
            "cryptocurrency.pipelines.CryptocurrencyPipeline": 300
        }
    }
    def parse(self, response):

        items = CryptocurrencyItem()

        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        driver = webdriver.Firefox(executable_path=GECKODRIVER,
                                   firefox_options=options,
                                   firefox_binary=FIREFOX_BINARY)
        for i in json.loads(response.body):

            data = etree.HTML(i)
            table = data.xpath("//div[@class = 'cmc-table__table-wrapper-outer']/div/table/tbody/tr")

        # driver.get(response.url)
        # # Implicit wait
        # driver.implicitly_wait(10)
        # # Explicit wait
        # wait = WebDriverWait(driver, 5)
        # wait.until(EC.presence_of_element_located((By.CLASS_NAME, "cmc-table__table-wrapper-outer")))
        # table = driver.find_elements_by_xpath("//div[@class = 'cmc-table__table-wrapper-outer']/div/table/tbody/tr")

            for line in table:
                items["A_DATE"] = line.xpath(".//td[1]/div/text()")[0]
                items["B_OPEN"] = line.xpath(".//td[2]/div/text()")[0]
                items["C_HIGH"] = line.xpath(".//td[3]/div/text()")[0]
                items["D_LOW"] = line.xpath(".//td[4]/div/text()")[0]
                items["E_CLOSE"]  = line.xpath(".//td[5]/div/text()")[0]
                items["F_VOLUME"] = line.xpath(".//td[6]/div/text()")[0]
                items["H_MARKETCAP"] = line.xpath(".//td[7]/div/text()")[0]

                yield items
            pass
