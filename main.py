from selenium import webdriver
from selenium.webdriver.support.select import Select
import time
import os
import re
import shutil


# 폴더정보를 넘겨주면 해당 폴더가 있는지 확인해서 폴더가 존재하지 않을 경우 폴더 생성하는 함수
def make_folder(folder_name):
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)

# 기존 파일을 목표하는 곳으로 보내는 함수
def move_file(source, destination):
    files = os.listdir(source)
    for f in files:
        shutil.move(source+'//'+ f, destination+'//'+ f)

# 게시물이 생겨난 일시를 폴더로 생성하는 
def make_file(date, id, count, path):
    f = open(path + "//"+ str(count) + ".txt", 'a')
    data = "일시 : " + date + " task_id: " + id
    f.write(data)
    f.close()



# 한 페이지 파일 원본파일 결과 파일 다운로드
def down_onepage(count):
    for i in range(1, 26):
        pass_exelist = ['eml', 'txt', 'html', 'Unknown', 'zip']
        pass_statuslist = ['바이러스', '미지원 파일', '확장자 위변조', '분석 불가', '암호화', '타임아웃', '접근 불가']
        try:
            extension = driver.find_element_by_xpath(
                '//*[@id="content"]/div[1]/div/div[2]/table/tbody/tr[' + str(i) + ']/td[7]')
            status = driver.find_element_by_xpath(
                '//*[@id="content"]/div[1]/div/div[2]/table/tbody/tr[' + str(i) + ']/td[3]')
        except:
            break

        if (extension.text in pass_exelist):
            pass
        elif (status.text in pass_statuslist):
            pass
        else:

            driver.find_element_by_xpath(
                '//*[@id="content"]/div[1]/div/div[2]/table/tbody/tr[' + str(i) + ']/td[11]/button').click()
            time.sleep(1)
            driver.find_element_by_xpath(
                '//*[@id="content"]/div[1]/div/div[2]/table/tbody/tr[' + str(i) + ']/td[12]/button').click()
            time.sleep(1)
            driver.find_element_by_xpath(
                '//*[@id="content"]/div[1]/div/div[2]/table/tbody/tr[' + str(i) + ']/td[5]').click()
            time.sleep(1)
            task_date = driver.find_element_by_xpath('//*[@id="basic-info-tab"]/div/dl[1]/dd').text
            task_id = driver.find_element_by_xpath('//*[@id="basic-info-tab"]/div/dl[2]/dd').text

            date = re.sub(r"[^a-zA-Z0-9]", "", task_date)
            date = date[:8]
            # task_date.text

            driver.find_element_by_xpath('//*[@id="close_btn"]').click()

            path = r"C://Users//지란지교//downdocument//" + date
            path2 = path + "//" + str(count)
            make_folder(path)
            make_folder(path2)
            time.sleep(1)
            # print(task_id)
            # print(task_date)
            make_file(task_date, task_id, count,path2)
            move_file(r"C://Users//지란지교//SaniTox", path2)

            # move_file(r"C://Users//지란지교//downdocument//", 'C://Users//지란지교//downdocument//20210101')
            # move_file(path, path2)
            time.sleep(1)
            count += 1


    return count

start_year, start_month, start_day = input("다음과 같이 시작 날짜를 입력해주세요.ex) 2021 3 1").split(" ")

# start_year='2021'
# start_month = '1'
# start_day = '1'
ID = os.environ['ID']
PW = os.environ['PW']
end_month = '1'
end_day = '1'

# 셀레니움 라이브러리 기본 작업
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

# 경로 변경 test
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": r'C:\Users\지란지교\SaniTox',
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True
})

driver = webdriver.Chrome(r'C:\Users\지란지교\PycharmProjects\stdash\chromedriver.exe', options=chrome_options)
driver.set_window_size(1200, 800)
driver.implicitly_wait(3)

# target 페이지 가져오기
driver.get('http://10.52.100.220/accounts/login/')

# target website 로그인 하기
driver.find_element_by_name('email').send_keys(ID)
driver.find_element_by_name('password').send_keys(PW)
driver.find_element_by_xpath('//*[@id="login"]/div/div/button').click()
driver.implicitly_wait(3)
# 로그 탭 클릭
driver.find_element_by_xpath('//*[@id="header"]/div/div[2]/ul/li[2]/a').click()

# 기간 버튼 클릭
driver.find_element_by_xpath('//*[@id="id_date_4"]').click()

# #시작 날짜 입력
from_dp = driver.find_element_by_xpath('//*[@id="id_log_s_date"]')
from_dp.click()

time.sleep(1)

datepicker_year = driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/span').text

while(datepicker_year!=start_year):
  if (start_year < datepicker_year):
     from_month = driver.find_element_by_xpath("//div/select[@class='ui-datepicker-month']")
     selected_from_month = Select(from_month)
     selected_from_month.select_by_visible_text("1월")
     driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/a[1]').click()
     datepicker_year = driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/span').text
  elif (start_year < datepicker_year):
     from_month = driver.find_element_by_xpath("//div/select[@class='ui-datepicker-month']")
     selected_from_month = Select(from_month)
     selected_from_month.select_by_visible_text("12월")
     driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/a[1]').click()
     datepicker_year = driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[1]/div/span').text
  else:
     pass

from_month = driver.find_element_by_xpath("//div/select[@class='ui-datepicker-month']")
selected_from_month = Select(from_month)
selected_from_month.select_by_visible_text(start_month + "월")
time.sleep(1)

from_day = driver.find_element_by_xpath(
    "//td[not(contains(@class,'ui-datepicker-month'))]/a[text()='" + start_day + "']")
from_day.click()
time.sleep(1)

# 끝 날짜 입력
driver.find_element_by_xpath('//*[@id="id_log_e_date"]').click()

time.sleep(1)

from_month = driver.find_element_by_xpath("//div/select[@class='ui-datepicker-month']")
selected_from_month = Select(from_month)
selected_from_month.select_by_visible_text(end_month + "월")
time.sleep(1)

# 몇시 몇분 입력
from_day = driver.find_element_by_xpath("//td[not(contains(@class,'ui-datepicker-month'))]/a[text()='" + end_day + "']")
from_day.click()
time.sleep(1)

select = Select(driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[2]/dl/dd[2]/div/select'))
select.select_by_value('0')

select = Select(driver.find_element_by_xpath('//*[@id="ui-datepicker-div"]/div[2]/dl/dd[3]/div/select'))
select.select_by_value('10')

# 검색 버튼 클릭
driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/form/div/dl[2]/dl/button').click()

# 페이지 리스트 뽑아오기.

pagelist = driver.find_elements_by_css_selector('#content > div.contents > div > ul > select > option')
# 페이지 리스트에 저장
pagelistnumber = len(pagelist)

print(pagelistnumber)

count: int = 0

# 페이지 리스트 만큼 한페이지 다운로드 실행.
for pagenumber in range(1, pagelistnumber+1):
    select = Select(driver.find_element_by_xpath('//*[@id="content"]/div[1]/div/ul/select'))
    select.select_by_visible_text(str(pagenumber))
    time.sleep(1)
    pagecount = down_onepage(count)
    # print(pagecount)
    count += pagecount
    time.sleep(1)
