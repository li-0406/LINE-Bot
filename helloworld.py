import random

ans = random.randint(0, 10)
print("請猜一個0~10的數字")
play = True
times = 0
while play:
    try:
        guess = int(input("來隨便猜一個數字吧: "))
    except:
        print("錯誤")
        play = False
    else:
        times = times + 1  # 每猜一次就要+1
        if guess > ans:
            print("喔你猜得太大囉")
        elif guess < ans:
            print("喔你猜得太小囉")
        else:
            print("恭喜你猜對了！")
            play = False
    finally:
        print("你猜了" + str(times) + "次")
