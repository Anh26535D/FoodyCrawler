import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchAttributeException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options



from time import sleep
import numpy as np
import random
import pandas as pd

count = 0

chrome_options = Options()

with open('links.txt', 'r') as file:
    with open("foody_1.json", "a", encoding="utf-8") as outfile:
        for urls in file:
            count += 1

            # ae tự đổi chỗ này nhé, file foody.json kia tôi chạy được 500 link rồi
            # if count < 500:
            #     continue
            
            try:
                info = []
                url = urls.replace("https://shopeefood.vn/", "")
                if count == 10:
                    break
                url_foody = "https://www.foody.vn/" + url
                url_shopeefood = "https://shopeefood.vn/" + url

                print("đang xử lý url:", count)
                chrome_options.add_argument("--disable-gpu")

                # Khởi tạo trình duyệt Chrome với các tùy chọn đã cấu hình
                driver = webdriver.Chrome("chromedriver.exe", options=chrome_options)

                driver.get(url_shopeefood)
                sleep(random.randint(3, 4))
                # Lướt xuống cuối trang
                browser_height = driver.execute_script("return window.innerHeight")

                temp_list = []
                while True:
                    # Lướt xuống một khoảng nhỏ
                    driver.execute_script("window.scrollBy(0, {})".format(browser_height))
                    
                    # Kiểm tra xem trình duyệt đã đến cuối trang hay chưa
                    end_of_page = driver.execute_script(
                        "return (window.innerHeight + window.pageYOffset) >= document.body.offsetHeight;"
                    )
                    
                    if end_of_page:
                        # Trình duyệt đã đến cuối trang, thoát khỏi vòng lặp
                        break

                    # Thu thập thông tin về món ăn và giá cả
                    foods = driver.find_elements(By.CSS_SELECTOR, ".item-restaurant-name")
                    foods = [food.text for food in foods]

                    prices = driver.find_elements(By.CSS_SELECTOR, ".current-price")
                    prices = [price.text for price in prices]

                    # Lặp qua từng cặp món ăn và giá cả
                    for food, price in zip(foods, prices):
                        # Kiểm tra xem món ăn và giá cả đã tồn tại trong danh sách tạm thời chưa
                        if (food, price) not in temp_list:
                            # Thêm vào danh sách chính
                            temp_list.append((food, price))
                            # Thực hiện xử lý khác (nếu cần)
                
                # driver.quit()

                food_price_pairs = [{"food": food, "price": price} for food, price in temp_list]

                driver.get(url_foody)
                sleep(random.randint(1, 2))
                titles = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/section/div/div/div/div[1]/div/div[2]/div[3]/div/div/div[3]/h1").text

                location = driver.find_element(By.CSS_SELECTOR, ".res-common-add")
                location = location.text    

                SoBinhLuan = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[1]/b").text
                TuyetVoi = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[2]/span/b").text
                Kha = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[3]/span/b").text
                TrungBinh = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[3]/span/b").text
                Kem = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[5]/span/b").text
                
                Score_ViTri = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[6]/div/table/tbody/tr[2]/td[3]/b").text
                Score_GiaCa = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[6]/div/table/tbody/tr[3]/td[3]/b").text
                Score_ChatLuong = driver.find_element(By.XPATH , "/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[6]/div/table/tbody/tr[3]/td[3]/b").text
                Score_PhucVu = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[6]/div/table/tbody/tr[5]/td[3]/b").text
                Score_KhongGian = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[6]/div/table/tbody/tr[6]/td[3]/b").text

                DanhGiaChung = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[2]/section/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div[1]/div/div[7]/div/span/b").text

                info.append({
                    "Title": titles,
                    "Vị trí": location,
                    "Đánh giá chung": DanhGiaChung,
                    "Số Bình Luận": SoBinhLuan,
                    "Tuyệt Vời": TuyetVoi,
                    "Khá tốt": Kha,
                    "Trung Bình": TrungBinh,
                    "kém": Kem,
                    "Điểm Vị Trí": Score_ViTri,
                    "Điểm Giá Cả": Score_GiaCa,
                    "Điểm chất lượng": Score_ChatLuong,
                    "Điểm Phục vụ":Score_PhucVu,
                    "Điểm Không Gian": Score_KhongGian,
                    "Đồ ăn của quán": food_price_pairs
                })
                
                # result.append(info)
                json.dump(info, outfile,indent=4, ensure_ascii=False)
                outfile.flush()
                driver.quit()
            except:
                with open("url_error.txt", 'a') as url_error:
                    url_error.write(url)


        
