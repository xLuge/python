# 导入所需库
import pandas as pd
import time
from selenium import webdriver

# 打开chrome
browser = webdriver.Chrome()

def login_douban():
    """
    功能：自动登录豆瓣
    """
    # 进入登录页面
    login_url = 'https://accounts.douban.com/passport/login?source=movie'
    browser.get(login_url)

    # 点击密码登录
    browser.find_element_by_xpath('//*[@id="account"]/div[2]/div[2]/div/div[1]/ul[1]/li[2]').click()
    # 输入账号和密码
    username = browser.find_element_by_xpath('//*[@id="username"]')
    username.send_keys('你的账号')
    password = browser.find_element_by_xpath('//*[@id="password"]')
    password.send_keys('你的密码')

    # 点击登录
    browser.find_element_by_xpath('//*[@id="account"]/div[2]/div[2]/div/div[2]/div[1]/div[4]/a').click()


def get_douban_comment(movie_id):
    # 总表
    df_all = pd.DataFrame()

    for page_num in range(25):
        # 获取URL
        url = f'https://movie.douban.com/subject/{movie_id}/comments?start={page_num*20}&limit=20&sort=new_score&status=P'

        # 打印进度
        print(f'正在获取第{page_num+1}页的信息')

        # 发起请求
        browser.get(url)

        # 休眠一秒
        time.sleep(1)

        # 获取用户名
        user_name = [i.text for
                     i in browser.find_elements_by_xpath('//div[@class="comment-item"]//span[@class="comment-info"]/a')]
        # 获取主页URL
        page_url = [i.get_attribute('href')
                    for i in browser.find_elements_by_xpath('//div[@class="comment-item"]//span[@class="comment-info"]/a')]
        # 获取评分
        rating_num = [i.get_attribute('title')
                      for i in browser.find_elements_by_xpath('//div[@class="comment-item"]//span[@class="comment-info"]/span[2]')]
        # 获取评论时间
        comment_time = [i.get_attribute('title')
                        for i in browser.find_elements_by_xpath('//div[@class="comment-item"]//span[@class="comment-info"]/span[last()]')]
        # 短评信息
        short_comment = [i.text
                         for i in browser.find_elements_by_xpath('//div[@class="comment-item"]//span[@class="short"]')]
        # 投票次数
        votes_num = [i.text
                     for i in browser.find_elements_by_xpath('//div[@class="comment-item"]//span[@class="votes"]')]

        # 存储数据
        df_one = pd.DataFrame({
            'user_name': user_name,
            'page_url': page_url,
            'rating_num': rating_num,
            'comment_time': comment_time,
            'short_comment': short_comment,
            'votes_num': votes_num
        })

        # 追加
        df_all = df_all.append(df_one, ignore_index=True)


    return df_all


def get_city_names(url_list):
    # 创建一个空列表，用于存储位置和签名数据
    city_names = []

    for index_num, url in enumerate(url_list):
        print(f'正在获取第{index_num+1}个用户的信息')

        # 发起请求
        browser.get(url)

        # 休眠1秒
        time.sleep(1)

        # 获取地址
        try:
            city_one = browser.find_element_by_xpath('//div[@class="user-info"]/a').text
            city_names.append(city_one)
        except Exception as e:
            print(e)
            city_names.append('未知')

    return city_names


# 先登录豆瓣
login_douban()

# 三十而已
df = get_douban_comment(movie_id='26608230')

# 获取城市信息
# city_names = get_city_names(url_list=df['page_url'])
# df['city_name'] = city_names

# 读出数据
df.to_excel('./data/三十而已豆瓣短评7.22.xlsx', index=False)
