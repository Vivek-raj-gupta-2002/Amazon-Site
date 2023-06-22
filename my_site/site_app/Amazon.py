import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pickle
from fake_useragent import UserAgent
import os


headers = {
        'User-Agent': 'PostmanRuntime/7.32.3',
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Upgrade-Insecure-Requests': '1',
}

class Amazon:

    headers = headers

    def __init__(self) -> None:
        # initiated the session
        self.session = requests.Session()


    # sending the get request to Amazon server
    def send_request(self, url: str) -> BeautifulSoup:

        ua = UserAgent(browsers=['edge', 'chrome'])

        headers['User-Agent'] = ua.random
        # checking the url is valid or not
        my_url = urlparse(url) 

        # to 
        self.url_ = my_url

        if 'amazon' not in my_url.netloc or 'dp' not in my_url.path:# checking for the validity of link
            raise Exception('Invalid Link')
        
        # loding the cookies from the file saved
        file = self.load_cookies()

        # checking if cookies exists
        if file != 0:
            # adding cookies to the header
            headers['cookie'] = file
        
        self.session.headers.update(
            headers
        )
        
        # sending the get request
        self.get_request = self.session.get(url)

        # if not OK
        if '200' not in str(self.get_request):# if request is not 'OK'
            raise Exception(self.get_request.status_code)
        
        # saving the cookies
        self.save_cookies(self.session.cookies)

        return BeautifulSoup(self.get_request.content, 'html.parser')
    
    def get_asin(self, url) -> str:
        path = url.path

        if path != '':
            path = path.split('/')

        try:
            path = path[path.index('dp') + 1]
        except:
            path = ''

        return path


    def product_details(self, soup: BeautifulSoup) -> dict:

        return {
            'title': self.get_title(soup),
            'rating': self.get_rating(soup),
            'review': self.get_review_count(soup),
            'isAvaliable': self.get_availability(soup),
            'price': self.get_price(soup),
            'mrp': self.get_mrp(soup),
            'seller': self.get_seller(soup),
            'ASIN': self.get_asin(self.url_),
            'First_date': self.get_date(soup)
        }
        
    
    def get_title(self, soup: BeautifulSoup) -> str:

        try:
            # get the title of the Product
            title = soup.find('span', id='productTitle').text
            title = " ".join(title.strip().split())

        except:
            # when no title found
            title = ''

        return title
    

    # Function to extract Product Price
    def get_price(self, soup: BeautifulSoup) -> str:

        try:
            price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()

        except AttributeError:

            try:
                # If there is some deal price
                price = soup.find("div", attrs={'id':'corePrice_feature_div'}).string.strip()

            except:		
                price = ""	

        return price
    
    def get_seller(self, soup: BeautifulSoup) -> str:
        try:
            sel = soup.find('div', id='merchant-info').find('a').text
        except:
            sel = ''

        return sel


    # getting the mrp of the product
    def get_mrp(self, soup: BeautifulSoup) -> str:
        try:
            price = soup.find("span", attrs={'class':'a-price a-text-price'})

            price = price.find("span", attrs={'class':'a-offscreen'}).text

        except:
            price = ''

        return price

    def get_rating(self, soup: BeautifulSoup) -> str:

        try:
            rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
            
        except AttributeError:
            
            try:
                rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
            except:
                rating = ""	

        return rating
    
    def get_date(self, soup):
        try:
            review_count = soup.find("div", attrs={'id':'mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE'})
            
            review_count = review_count.find('span', attrs={'class': 'a-text-bold'}).text

        except AttributeError:
            review_count = ""	

        return review_count

    
    # Function to extract Number of User Reviews
    def get_review_count(self, soup: BeautifulSoup) -> str:
        try:
            review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
            
        except AttributeError:
            review_count = ""	

        return review_count

    # Function to extract Availability Status
    def get_availability(self, soup: BeautifulSoup) -> str:
        try:
            available = soup.find("div", attrs={'id':'availability'})
            available = available.find("span").string.strip()

        except AttributeError:
            available = "Not Available"	

        return available

    # saving the cookies
    def save_cookies(self, cook) -> bool:
        with open('amazon.pkl', 'wb') as file:
            pickle.dump(cook, file)
        return True

    # geting the data from saved cookies file
    def load_cookies(self):
        try:
            with open('amazon.pkl', 'r') as file:
                return pickle.load(file)
        except:
            return 0
        
    
    def close_session(self) -> None:# deleting the cookies and closing the sessions
        # closing the session
        self.session.close()

        # deleting the cookies
        file = 'amazon.pkl'

        if os.path.exists(file):
            os.remove(file)
            return
        raise Exception('File Not Exitst')
