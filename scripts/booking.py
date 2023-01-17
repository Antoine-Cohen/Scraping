from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time


url = """https://www.booking.com/searchresults.en-us.html?ss=Madrid+City+Center%2C+
Madrid%2C+Comunidad+de+Madrid%2C+Spain&map=1&efdco=1&label=gen173nr-
1FCAEoggI46AdIM1gEaE2IAQGYATG4ARfIAQ_YAQHoAQH4AQKIAgGoAgO4AveNip4GwAIB0gIkZjA3Nm
E2MDMtNTY2OS00OTVmLWI2ZDEtOGJjNzc4NzNlOTM22AIF4AIB&aid=304142&lang=en-us&sb=1&src_
elem=sb&src=index&dest_id=176&dest_type=district&ac_position=0&ac_click_type=b&ac_lang
code=xu&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=13424b3bc5f
d01e3&ac_meta=GhAxMzQyNGIzYmM1ZmQwMWUzIAAoATICeHU6Bk1hZHJpZEAASgBQAA%3D%3D&checkin=2023-01-
23&checkout=2023-01-25&group_adults=2&no_rooms=1&group_children=0&sb_travel_purpose=leisure#map_closed"""

def launch_driver(url):
    driver = webdriver.Firefox()
    driver.get(url)
    return driver

def try_element_text(driver,by,criteria):
    try:
        return driver.find_element(by,criteria).text
    except:
        return None

def try_element(driver,by,criteria):
    try:
        return driver.find_element(by,criteria)
    except:
        return driver

def get_box_info(box,boxes_infos):
    boxes_infos['title'].append(try_element_text(box,By.XPATH,'.//div[@data-testid="title"]'))
    boxes_infos['price'].append(try_element_text(box,By.XPATH,'.//span[@data-testid="price-and-discounted-price"]'))
    boxes_infos['previous_price'].append(try_element_text(box,By.XPATH,'.//span[@class="c5888af24f e729ed5ab6"]'))
    boxes_infos['location_score'].append(try_element_text(box,By.XPATH,'.//a[@data-testid="secondary-review-score-link"]'))

    return boxes_infos

def switch_new_window(driver,wait):
    wait.until(EC.number_of_windows_to_be(2))
    driver.switch_to.window(driver.window_handles[1])

def close_back_window(driver):
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def accept_cookies(driver):
    driver.find_element(By.ID,"onetrust-accept-btn-handler").click()

def get_property_infos(driver,pp_infos):
    pp_infos['property_type'].append(try_element_text(driver,By.XPATH,'//span[@data-testid="property-type-badge"]'))
    pp_infos['address'].append(try_element_text(driver,By.XPATH,'//span[@data-node_tt_id="location_score_tooltip"]'))
    pp_infos['score'].append(try_element_text(driver,By.XPATH,'//div[@class="b5cd09854e d10a6220b4"]'))
    pp_infos['score_label'].append(try_element_text(driver,By.XPATH,'//div[@class="b5cd09854e f0d4d6a2f5 e46e88563a"]'))
    pp_infos['n_reviews'].append(try_element_text(driver,By.XPATH,'//div[@class="d8eab2cf7f c90c0a70d3 db63693c62"]'))
    pp_infos['description'].append(try_element_text(driver,By.ID,'property_description_content'))

    appliances = try_element(driver,By.XPATH,'//div[@data-testid="property-highlights"]')
    appliances = appliances.find_elements(By.XPATH,'.//div[@role="cell"]')
    appliances = [ap.text for ap in appliances]
    pp_infos['appliances'].append(','.join(appliances))

    pop_fac = driver.find_elements(By.XPATH,'//span[@class="db312485ba"]')
    pop_fac = [fac.text for fac in pop_fac]
    pp_infos['popular_facilities'].append(','.join(pop_fac))


    score_cat = try_element(driver,By.XPATH,'//div[@data-capla-component="b-property-web-property-page/PropertyReviewSubscores"]')
    cats = score_cat.find_elements(By.XPATH,'.//span[@class="d6d4671780"]')
    cats = [cat.text for cat in cats]
    scores = score_cat.find_elements(By.XPATH,'.//div[@class="ee746850b6 b8eef6afe1"]')
    scores = [score.text for score in scores]

    cat_scores = dict(zip(cats,scores))
    pp_infos['score_categories'].append(cat_scores)

    return pp_infos


def get_page_infos(driver,infos):
    wait = WebDriverWait(driver, 10)
    boxes = driver.find_elements(By.XPATH,'//div[@data-testid="property-card"]')
    time.sleep(5)
    for box in boxes:
        infos = get_box_info(box,infos)
        box.find_element(By.XPATH,'.//a[@data-testid="title-link"]').click()
        switch_new_window(driver,wait)
        time.sleep(10)
        infos = get_property_infos(driver,infos)
        close_back_window(driver)
        time.sleep(10)
    
    infos_df = pd.DataFrame(infos)
    return infos_df

def get_n_pages(driver):
    n_pages = driver.find_element(By.XPATH,'/html/body/div[4]/div/div[3]/div[1]/div[1]/div[4]/div[2]/div[2]/div/div/div/div[5]/div[2]/nav/div/div[2]/ol/li[6]/button').text
    return int(n_pages)

def get_all_infos(driver):
    attributes = ['title','price','previous_price','location_score','property_type','address','score','score_label','n_reviews','description','appliances','popular_facilities','score_categories']
    values = [[] for i in range(len(attributes))]
    infos = dict(zip(attributes,values))
    accept_cookies(driver)
    infos_df = pd.DataFrame()
    n_pages = get_n_pages(driver)
    for i in range(n_pages):
        infos = dict(zip(attributes,values))
        page_info = get_page_infos(driver,infos)
        if i == 0:
            page_info.to_csv('./csvs/booking_all.csv',index=False)
        else:
            page_info.to_csv('./csvs/booking_all.csv',index=False,header=False,mode = 'a')
        driver.find_element(By.XPATH,'//button[@aria-label="Next page"]').click()

        time.sleep(5)

        







driver = launch_driver(url)
time.sleep(5)
get_all_infos(driver)


# driver.close()
