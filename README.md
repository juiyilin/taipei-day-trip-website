# 旅遊電商網站
![](https://user-images.githubusercontent.com/52588493/122661681-719ceb00-d1bf-11eb-881f-033fc0e95e5a.png)  

## 資料庫設計  
![](https://user-images.githubusercontent.com/52588493/128993719-79256b48-a570-488b-84fb-31a64abf597c.png)  

## 使用技術
- Frontend: HTML, css, JavaScript ( RWD )  
- Backend: Python ( Flask )  
- Database: MySQL  
- Amazon Web Service: EC2    
- TapPay ( 第三方金流 )  
##  

網站頁面使用[台北各景點資料](/data/taipei-attractions.json)串接 TapPay 金流服務，佈署於雲端伺服器 AWS EC2，將使用者與訂單資訊儲存於 EC2 上之 MySQL 中，採 RESTful API 架構取得所需資料。  

網址：[http://35.72.79.89:3000/](http://35.72.79.89:3000/)(已關閉)  
測試帳號：test@test.test  
測試密碼：test  

Tappay 測試卡號 : 4242 4242 4242 4242  
測試過期時間 : 01/23  
測試末三碼 : 123  

## 頁面概觀
登入前畫面  
![登入前畫面](https://user-images.githubusercontent.com/52588493/122664861-6f925680-d1d6-11eb-9720-ddd6055f4f7e.png)  

登入後畫面 ( 選單變化 )  
![登入後畫面](https://user-images.githubusercontent.com/52588493/122664877-8e90e880-d1d6-11eb-891e-a900f314d515.png)  
#  
景點搜尋  
![景點搜尋](https://user-images.githubusercontent.com/52588493/122665460-eaa93c00-d1d9-11eb-998e-b7b93d20c8ff.png)

景點介紹  
![image](https://user-images.githubusercontent.com/52588493/122665341-3effec00-d1d9-11eb-8f8c-aa928055d7da.png)
#  
付款畫面  
![image](https://user-images.githubusercontent.com/52588493/122665418-a453dd00-d1d9-11eb-9f0d-b94a28433be1.png)  

付款完成  
![image](https://user-images.githubusercontent.com/52588493/122665495-27753300-d1da-11eb-8828-27bbea6ffaf1.png)
#  
訂購紀錄  
![image](https://user-images.githubusercontent.com/52588493/122665523-483d8880-d1da-11eb-96f5-78ab99b7ee99.png)

查看訂單  
![image](https://user-images.githubusercontent.com/52588493/122665567-876bd980-d1da-11eb-91c7-73a863ea50ea.png)
