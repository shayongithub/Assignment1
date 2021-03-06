# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import scrapy
from scrapy import signals
from scrapy import Request
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import loguru
import time
import random
import json

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

#Required credential
BROWSER_EXE = 'C:\Program Files\Mozilla Firefox/firefox.exe'
GECKODRIVER = 'D:\geckodriver.exe'
FIREFOX_BINARY = FirefoxBinary(BROWSER_EXE)

#Code to disable notifications pop up of Chrome Browser
PROFILE = webdriver.FirefoxProfile()
#PROFILE.DEFAULT_PREFERENCES['frozen']['javascript.enabled] = False
PROFILE.set_preference("dom.webnotifications.enabled", False)
PROFILE.set_preference("app.update.enabled", False)
PROFILE.update_preferences()

class RotateAgentMiddleware(object):

    def process_request(self, request, spider):

        # webdriver setting
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')

        # webdriver request
        driver = webdriver.Firefox(executable_path=GECKODRIVER,
                                   firefox_options = options,
                            firefox_binary=FIREFOX_BINARY)
        driver.get("https://deviceatlas.com/blog/list-of-user-agent-strings")
        time.sleep(1)

        # real time random select user agent from website
        agent_list = driver.find_elements_by_xpath("//td")
        agent = (random.choice(agent_list)).text
        loguru.logger.info("Hold Agent {agent}".format(agent=agent))
        driver.quit()

        # hold user agent
        request.headers["User-Agent"] = agent

class RotateProxyMiddleware(object):

    def process_request(self, request, spider):
        # webdriver setting
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')

        # webdriver request
        driver = webdriver.Firefox(executable_path=GECKODRIVER,
                                   firefox_options=options,
                                   firefox_binary=FIREFOX_BINARY)
        driver.get("http://free-proxy-list.net")
        time.sleep(1)

        # real time random select free proxy from website
        row = int(random.randint(1, 20))
        ip = driver.find_element_by_xpath("//tbody/tr[{row}]/td[1]".format(row=row)).text
        port = driver.find_element_by_xpath("//tbody/tr[{row}]/td[2]".format(row=row)).text
        proxy = "{ip}:{port}".format(ip=ip, port=port)
        loguru.logger.info("Hold Proxy {proxy}".format(proxy=proxy))
        driver.quit()

        # hold proxy
        request.meta["proxy"] = proxy
class CryptocurrencyMiddleware(object):

    def process_request(self, request, spider):

        data = []
        url = request.url

        # webdriver setting
        options = webdriver.FirefoxOptions()
        options.add_argument('--headless')
        # options.add_argument('--proxy-server=%s' % request.meta["proxy"])
        options.add_argument('--user-agent=%s' % request.headers["User-Agent"])

        # webdriver request
        driver = webdriver.Firefox(executable_path=GECKODRIVER,
                                   firefox_options=options,
                                   firefox_binary=FIREFOX_BINARY)
        driver.set_window_size(1440, 800)
        driver.delete_all_cookies()
        driver.get(url)
        loguru.logger.info("Hold URL {url}".format(url=url))
        data.append(driver.page_source)
        # clean popup
        try:
            popup_xpath = (
                './/div[@class = "cmc-cookie-policy-banner__close"]'
            )
            popup_element = WebDriverWait(driver, 60).until(
                EC.element_to_be_clickable((By.XPATH, popup_xpath))
            )
            loguru.logger.warning(popup_element.text)
            popup_element.click()
            time.sleep(5)

            # Crawl from 3 years ago start from Nov 17 2017 to now
            #Set start date
            start_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[1]/div[2]/div[3]/div/ul[2]/li[5]/div/div/div[1]/div/div/span/span/div/div[1]/input'))
            )

            start_element.send_keys(Keys.BACKSPACE * 12)
            start_element.send_keys("Nov 17, 2017")
            start_element.send_keys(Keys.RETURN)
            time.sleep(5)

            # Set end date
            end_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div[1]/div[2]/div[3]/div/ul[2]/li[5]/div/div/div[1]/div/div/span/span/div/div[2]/input'))
            )

            end_element.send_keys(Keys.BACKSPACE * 12)
            end_element.send_keys("Oct 18, 2020")
            # end_element.send_keys(Keys.RETURN)

            time.sleep(5)
            #driver.refresh()
            url = driver.current_url
            loguru.logger.info("Hold URL {url}".format(url = url))

            data.append(driver.page_source)
        except:
            driver.quit()

        return scrapy.http.HtmlResponse(url=url,
                                        status=200,
                                        body=json.dumps(data).encode('utf-8'),
                                        encoding='utf-8')

class CryptocurrencySpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CryptocurrencyDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)