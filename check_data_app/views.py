from django.shortcuts import render , redirect , HttpResponse
import bs4 as bs
import urllib.request
from selenium  import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .send_email import sendEmail
import time
# Create your views here.



def Home(request):
    if request.method == 'POST':
        country = request.POST.get('text' , '')
        checkWeb(country=country)
    return render(request , 'home.html',)
    
def checkWeb(country):
        try:
            driver = webdriver.Chrome()
            driver.get("https://evisaforms.state.gov/Instructions/ACSSchedulingSystem.asp")
            driver.implicitly_wait(25)
            countries = driver.find_element(By.NAME , "CountryCodeShow")
            dropCountry = Select(countries)
            dropCountry.select_by_value(country)
            city = driver.find_element(By.NAME , "PostCodeShow")
            dropCity = Select(city)
            dropCity.select_by_index('1')
            btn = driver.find_element(By.NAME , "Submit")
            btn.click()
            
            # page 2 click button
            btn2 = driver.find_element(By.XPATH , "//input[@value='Make Appointment!']")
            btn2.click()
            
            # page 3 click radio button and click checkbox and click button submit
            # click radio button
            radio = driver.find_element(By.XPATH , "//input[@value='AA']")
            radio.click()
            # click checkbox button
            checkbox = driver.find_element(By.NAME , "chkbox01")
            checkbox.click()
            # click button submit
            btn3 = driver.find_element(By.XPATH , "//input[@value='Submit']")
            btn3.click()
            url =  driver.page_source
            soup = bs.BeautifulSoup(url , 'html.parser')
            listTd = soup.find_all("td" , class_="formfield" , bgcolor="#ffffc0")
            countAvailable = 0

            for td in listTd:
                    countAvailable = countAvailable + 1

            if listTd:
                    print("The list is not empty")
                    sendEmail("قم بمراجعة مواعيد السفارة هناك مواعيد متاحة في "+str(countAvailable)+"أيام")
                    print(countAvailable)
            else:
                    print("the list empty")

            # await 5 second and exit the browser
            time.sleep(5)
            driver.quit() 
            
        except Exception as e:
            print(e)
            driver.quit()
    