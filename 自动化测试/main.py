from selenium import webdriver
from selenium.webdriver.common.by import By
from collections import defaultdict
import time

# 初始化驱动
driver = webdriver.Chrome()
# driver.set_window_size(1920, 1080)
# 最大化窗口
driver.maximize_window()
# 访问登录页面
driver.get("http://qdwj.k12lps.com:9099/czxs")
# 等待页面加载
driver.implicitly_wait(2)
# 输入用户名
username_input = driver.find_element(By.XPATH, "//input[@placeholder='账 号']")
username_input.send_keys("cs009")
username_input.screenshot('./image.png')
# 输入密码
password_input = driver.find_element(By.XPATH, "//input[@placeholder='密 码']")
password_input.send_keys("QDcs009")
# 点击登录按钮
login_button = driver.find_element(By.XPATH, "//div[@class='login-btn']/span")
login_button.click()
# 等待用户手动输入验证码
input("请手动输入验证码并完成验证后，按回车键继续...")


# 获取所有按钮并进行分组
def get_buttons_by_question():
    buttons = driver.find_elements(By.XPATH, "//input")
    questions = defaultdict(list)
    for button in buttons:
        question_name = button.get_attribute("name")
        if question_name:
            questions[question_name].append(button)
    return questions


for page in range(8):
    questions = get_buttons_by_question()  # 初次获取题目和选项

    # 遍历每组题目
    index = 0  # 记录当前遍历的题目位置
    while index < len(questions):  # 使用while循环动态调整题目列表
        question_name = list(questions.keys())[index]
        options = driver.find_elements(By.XPATH, f"//input[@name='{question_name}']")

        # 如果当前选项不可见，则跳过该题，并重新获取问题列表
        if not options:
            print(f'第{page + 1}页第{question_name}题不可见，跳过')
            questions = get_buttons_by_question()  # 重新获取问题，确保包含新增题目
            continue

        options[0].click()  # 点击第一个可见的选项
        print(f'第{page + 1}页第{question_name}题已填写')
        # time.sleep(0.1)

        index += 1  # 移动到下一个题目

    # 检查是否存在翻页按钮
    next_button = driver.find_elements(By.XPATH, '//*[@id="demonstration"]/div/button')
    if next_button:
        # 点击翻页按钮
        next_button[0].click()
        input('已自动填写完当前页的问卷，按回车键继续填写下一页...')
    else:
        # 如果没有翻页按钮，则点击提交按钮
        submit_button = driver.find_element(By.XPATH, '//*[@id="fill-container"]/main/button')
        submit_button.click()
        # 确认提交
        confirm_button = driver.find_element(By.XPATH, '/html/body/div[2]/div/div[3]/button[2]')
        confirm_button.click()
        print("问卷已提交")
        input('问卷已提交，按回车键结束程序...')

driver.quit()

