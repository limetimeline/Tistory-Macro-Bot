from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import os
import random

driver = webdriver.Chrome()
url = 'https://www.tistory.com/feed'
driver.get(url)

CommentList = ["좋은 글 보고 갑니다.", 
    "글을 잘 쓰시네요~ 좋은 하루보내세요!", 
    "좋은 글 보고가요~", 
    "좋은 정보 얻었어요~ 좋은 하루보내세요~", 
    "좋은 정보 얻어가요~ 또 올게요!", 
    "글을 참 잘 쓰시네요! 좋은 정보 감사합니다~", 
    "글을 잘 쓰시는 것 같아요! 좋은 글 감사합니다~", 
    "포스팅 잘봤습니다. 행복한 하루되세요.", 
    "공감 꾸욱하고 갑니다. 기분좋은 하루 보내세요.^^", 
    "언제나 좋은 글 올려주시네요. 잘 보고 갑니다. 감사합니다", 
    "오늘도 유익한 포스팅 잘보고 공감 살포시 누르고 갑니다! 좋은 하루 보내세요~"]
CategoryList = ["life", "travel", "culture", "it", "sports", "current"]

# 피드 리스트 생성 함수
def LoadPost(url):
    driver.get(url)

    # preloading 때문에 내려야함
    for c in range(0,25): # 25가 적당. 안바꿔도 됨 => 더보기 버튼이 작동해서..
        driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

    postList = []


    time.sleep(5)
    mArticle = driver.find_element(By.ID,'mArticle')
    
    # preloading 이후 더보기 버튼 클릭
    for i in range(10):
        divSectionList = mArticle.find_element(By.CLASS_NAME,'section_list')
        btn_more = divSectionList.find_element(By.CLASS_NAME, 'btn_more')
        driver.execute_script("arguments[0].click();", btn_more)
        time.sleep(1)

    ul = divSectionList.find_element(By.TAG_NAME, 'ul')

    for item in ul.find_elements(By.TAG_NAME, 'li'):
        aTagHref = item.find_element(By.TAG_NAME, 'a')

        div = item.find_element(By.TAG_NAME, 'div')
        desc_tit = div.find_element(By.CLASS_NAME, 'desc_tit')
        aTagDesc = desc_tit.find_element(By.TAG_NAME, 'a')

        if aTagHref.get_attribute('href')[-1] == '/':
            continue # 링크의 마지막이 /로 끝나면 out
        elif aTagHref.get_attribute('href').rsplit('/',1)[1].count('-') > 0:
            continue # 링크의 페이지 번호가 숫자가 아니라 '블로그-첫-글' 형식이면 out
        elif aTagHref.get_attribute('href').count('/') > 3:
            continue # 링크에 /가 3개 초과이면 out (https://limetimeline.tistory.com/32가 정상.)
        else:
            posts = []
            posts.append(aTagDesc.text) # 글 제목
            posts.append(aTagHref.get_attribute('href')) # 글 링크

            postList.append(posts)

    return postList        

def SaveList(postList):
    with open('postList.txt','w',encoding='UTF-8') as f:
        for post in postList:
            f.write(f'{post[0]}%^%{post[1]}\n')

def OpenList():
    postList = []
    f = open('./postList.txt','r',encoding='UTF8')
    lines = f.readlines()
    for line in lines:
        post = []
        line = line.replace('\n','')
        post.append(line.split('%^%')[0])
        post.append(line.split('%^%')[1])
        postList.append(post)
    f.close()
    return postList
    
# 댓글 쓰기 및 공감 누르기 Setting 함수
def Action(postList):
    while(True):
        answer = 0

        os.system('cls')
        print("------ 댓글 쓰기 및 공감 누르기 Setting ------")
        print(" *주의 : 크롬 창을 끄지 마세요!")
        print("1. 댓글만 쓰기")
        print("2. 공감만 누르기")
        print("3. 댓글도 쓰고, 공감도 누르기")
        print("4. 뒤로가기")

        answer = (int)(input("숫자를 입력하세요: "))
        
        if answer == 1: # 댓글만 쓰기
            for post in postList:
                driver.get(post[1])
                time.sleep(5)
                postNum = post[1].rsplit('/',1)[1]
                PostComment(postNum)
        elif answer == 2: # 공감만 누르기
            for post in postList:
                driver.get(post[1])
                time.sleep(5)
                postNum = post[1].rsplit('/',1)[1]
                PostLike(postNum)
        elif answer == 3: # 댓글도 쓰고, 공감도 누르기
            for post in postList:
                driver.get(post[1])
                time.sleep(5)
                postNum = post[1].rsplit('/',1)[1]
                PostComment(postNum)
                PostLike(postNum)
        elif answer == 4: # 뒤로가기
            return
        else:
            continue

# 공감 누르기 함수
def PostLike(postNum):
    try:
        postbtn_like = driver.find_element(By.CLASS_NAME,'postbtn_like')
        
        print('reaction-'+postNum)
        reaction = postbtn_like.find_element(By.ID,'reaction-'+postNum).click()
    except:
        pass

# 댓글 쓰기 함수
def PostComment(postNum):
    try:
        entryComment = driver.find_element(By.ID,'entry'+postNum+'Comment')

        randomComment = random.randrange(0, len(CommentList))

        print('entry'+postNum+'Comment')

        textarea = entryComment.find_element(By.TAG_NAME, 'textarea')
        textarea.send_keys(CommentList[randomComment])
        print(CommentList[randomComment])
        time.sleep(1)
        form = entryComment.find_element(By.TAG_NAME, 'form')


        Button = form.find_element(By.TAG_NAME, 'button')
        print(Button.text)
        Button.click()

        # Alert 창 대처
        alert = driver.switch_to.alert
        alert.dismiss()

    except:
        return
    
# 자동 구독 함수
def FollowerINC(categoryNum):
    print(f"{CategoryList[categoryNum]} 자동 구독 중...")
    driver.get("https://www.tistory.com/category/"+CategoryList[categoryNum])
    

    # 페이지 preloading 때문에 내려야함
    for c in range(0,30): # 원하는 만큼 지정하면 됨
        driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

    time.sleep(10) # 구독하기 로딩

    try:
        mArticle = driver.find_element(By.ID,'mArticle')
        divSectionList = mArticle.find_element(By.CLASS_NAME,'section_list')
        ul = divSectionList.find_element(By.TAG_NAME, 'ul')

        for item in ul.find_elements(By.TAG_NAME, 'li'):
            # 구독 버튼 누르기
            info_subscribe = item.find_element(By.CLASS_NAME, 'info_subscribe')
            button = info_subscribe.find_element(By.TAG_NAME, 'button')

            if str(button.get_attribute('innerHTML')) == "구독하기":
                # 블로그 이름 따기
                a = item.find_element(By.TAG_NAME, 'a')
                info_g = a.find_element(By.CLASS_NAME, 'info_g')
                txt_id = info_g.find_element(By.CLASS_NAME, 'txt_id')
                print(f"블로그 이름 : {txt_id.text} : {button.get_attribute('innerHTML')}")
                driver.execute_script("arguments[0].click();", button)
                time.sleep(1)
            else:
                continue
            
    except:
        pass


def StoryFeed():
    postList = []
    for categoryNum in range(len(CategoryList)):
        print(f"{CategoryList[categoryNum]} 리스트 추가 중...")
        driver.get("https://www.tistory.com/category/"+CategoryList[categoryNum])
        
        # 페이지 preloading 때문에 내려야함
        for c in range(0,50): # 원하는 만큼 지정하면 됨
            driver.find_element(By.TAG_NAME,'body').send_keys(Keys.PAGE_DOWN)
            time.sleep(1)

        time.sleep(10) # 구독하기 로딩

        try:
            mArticle = driver.find_element(By.ID,'mArticle')
            divSectionList = mArticle.find_element(By.CLASS_NAME,'section_list')
            ul = divSectionList.find_element(By.TAG_NAME, 'ul')

            for item in ul.find_elements(By.TAG_NAME, 'li'):
                # 구독 버튼 누르기
                info_subscribe = item.find_element(By.CLASS_NAME, 'info_subscribe')
                button = info_subscribe.find_element(By.TAG_NAME, 'button')

                if str(button.get_attribute('innerHTML')) == "구독하기":
                    # 블로그 이름 따기
                    a = item.find_element(By.TAG_NAME, 'a')

                    info_g = a.find_element(By.CLASS_NAME, 'info_g')
                    txt_id = info_g.find_element(By.CLASS_NAME, 'txt_id')

                    # print(a.get_attribute('href'))

                    if a.get_attribute('href')[-1] == '/':
                        continue # 링크의 마지막이 /로 끝나면 out
                    elif a.get_attribute('href').rsplit('/',1)[1].count('-') > 0:
                        continue # 링크의 페이지 번호가 숫자가 아니라 '블로그-첫-글' 형식이면 out
                    elif a.get_attribute('href').count('/') > 3:
                        continue # 링크에 /가 3개 초과이면 out (https://limetimeline.tistory.com/32가 정상.)
                    else:
                        posts = []
                        posts.append(txt_id.text) # 글 제목
                        posts.append(a.get_attribute('href')) # 글 링크
                        postList.append(posts)

                        # print(f"블로그 이름 : {txt_id.text} : {button.get_attribute('innerHTML')}")
                        time.sleep(1)
                else:
                    continue     
        except:
            pass
    
    return postList
        

def main():
    answer = 0

    mArticle = 'mArticle'
    divSectionList = 'section_list'

    postList = []

    while(True):
        os.system('cls')
        print("------ 자동 댓글/공감 프로그램 ------")
        print(" *주의 : 크롬 창을 끄지 마세요!, 반드시 로그인 한 상태에서 진행하세요.")
        print("1. 구독자 피드 리스트 생성")
        print("2. 댓글 쓰기 및 공감 누르기")
        print("3. 구독늘리기(최대 500개)")
        print("4. 스토리 피드 리스트 생성")
        print("5. PostList 불러오기(postList.txt)")

        answer = (int)(input("숫자를 입력하세요: "))
        
        if driver.current_url == url:
            if answer == 1:
                os.system('cls')
                print("피드 리스트 생성\n")
                postList = LoadPost(url)
                SaveList(postList)
                for i in postList:
                    print(f"title : {i[0]}, href : {i[1]}")
                driver.get(url)

            elif answer == 2:
                os.system('cls')
                if postList is not None:
                    print("댓글 쓰기 및 공감 누르기 \n")
                    Action(postList)
                    driver.get(url)
                else:
                    print("피드 리스트를 생성하고 오세요.")
                    driver.get(url)
                    time.sleep(3)
                    continue

            elif answer == 3:
                print("구독 늘리기\n")
                os.system('cls')
                for categoryNum in range(len(CategoryList)):
                    FollowerINC(categoryNum)
                driver.get(url)
            
            elif answer == 4:
                print("스토리 피드 리스트 생성")
                os.system('cls')
                
                postList = StoryFeed()
                SaveList(postList)
                for i in postList:
                    print(f"title : {i[0]}, href : {i[1]}")
                driver.get(url)
            elif answer == 5:
                print("postList 불러오기")
                os.system('cls')
                postList = OpenList() 
                
            # elif answer ==3:
            #     driver.get('https://wikibaff.tistory.com/67')
            #     PostComment('67')
            else:
                os.system('cls')
                continue
        else:
            print("로그인을 해주세요!!")
            driver.get(url)
            time.sleep(3)
            continue

if __name__ == "__main__":
    main()
