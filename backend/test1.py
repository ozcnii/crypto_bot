if __name__ == "__main__":
    import requests
    from config import DevelopmentConfig
    import json
    
    def oauth(id=0, username='test'):
        return requests.post(
            f"{DevelopmentConfig.HOST}/auth",
            data=json.dumps(
                {
                    "id":id,
                    "username":username
                }
            )
        ).json()['access_token']
         
    def users_get(token):
        headers = {'Authorization': f'Bearer {token}'}
        r=requests.get(f"{DevelopmentConfig.HOST}/users", headers=headers)
        print(r.json())
    
    def users_post(chat_id, username, token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0ZyI6ImJvdCJ9.WW6sya_8HSA0DWdaHC2uqj4HYSynUiEZzsbSBP4VKaI"): #Требует токена Telegram Bot
        headers = {'Authorization': f'Bearer {token}'}
        r=requests.post(f"{DevelopmentConfig.HOST}/users", headers=headers,
            data=json.dumps({
                "chat_id":chat_id,
                "username":username,
                "balance":1000,
                "league":"bronze",
                "boosters":[0,0,0,0,0],
            })
        )
        print(r.json())
        
    def users_delete(token):
        headers = {'Authorization': f'Bearer {token}'}
        r=requests.delete(f"{DevelopmentConfig.HOST}/users", headers=headers)
        print(r.json())  

    def users_put(token):
        headers = {'Authorization': f'Bearer {token}'}
        r=requests.put(f"{DevelopmentConfig.HOST}/users", headers=headers,
            data=json.dumps({
                "balance":1100,
            })
        )
        print(r.json())

    def users_get_getreflink(token):
        headers = {'Authorization': f'Bearer {token}'}
        r=requests.get(f"{DevelopmentConfig.HOST}/users/getreflink", headers=headers)
        print(r.json())
        
    def users_get_getref(token):
        headers = {'Authorization': f'Bearer {token}'}
        r=requests.get(f"{DevelopmentConfig.HOST}/users/getref", headers=headers)
        print(r.json())
        
    def users_get_topleader(token):
        headers = {'Authorization': f'Bearer {token}'}
        r=requests.get(f"{DevelopmentConfig.HOST}/users/topleader", headers=headers)
        print(r.json())
        
    def orders_get(token):
        headers = {'Authorization': f'Bearer {token}'}
        r=requests.get(f"{DevelopmentConfig.HOST}/orders", headers=headers)
        print(r.json())   
        
    def orders_open_post(token):
        headers = {'Authorization': f'Bearer {token}'}
        r=requests.post(f"{DevelopmentConfig.HOST}/orders/open", headers=headers,
            data=json.dumps({
                "priceinput":189.5,
                "amount":45.5,
                "position":"long",
                "leverage":10,
                "symbol":"SOL",
            })
        )
        print(r.json()) 
                
    def orders_update_post(token, id=1):
        headers = {'Authorization': f'Bearer {token}'}
        r=requests.post(f"{DevelopmentConfig.HOST}/orders/update/{id}", headers=headers,
            data=json.dumps({
                "coinprice":190.5,
            })
        )
        print(r.json())   
        
    def clans_get(token):
        headers = {'Authorization': f'Bearer {token}'}
        r=requests.get(f"{DevelopmentConfig.HOST}/clans", headers=headers)
        print(r.json()) 
         
    def clans_get_addmember(token, peer):
        headers = {'Authorization': f'Bearer {token}'}
        r=requests.get(f"{DevelopmentConfig.HOST}/clans/addmember/{peer}", headers=headers)
        print(r.json())  
        
    def clans_get_delmember(token, peer):
        headers = {'Authorization': f'Bearer {token}'}
        r=requests.get(f"{DevelopmentConfig.HOST}/clans/delmember/{peer}", headers=headers)
        print(r.json())  
        
    def clans_get_me(token):
        headers = {'Authorization': f'Bearer {token}'}
        r=requests.get(f"{DevelopmentConfig.HOST}/clans/me", headers=headers)
        print(r.json())  
        
    def clans_post(token):
        headers = {'Authorization': f'Bearer {token}'}
        r=requests.post(f"{DevelopmentConfig.HOST}/clans", headers=headers,
            data=json.dumps({
                "link":"https://t.me/sever_products",
            })
        )
        print(r.json()) 
    
    def league_get(token):
        headers = {'Authorization': f'Bearer {token}'}
        r=requests.get(f"{DevelopmentConfig.HOST}/league", headers=headers)
        print(r.json())  
         
    # <==== Тесты =====> #
    
    #Информация о пользователе
    id = 965240931
    username = 'severrrwork'
    
    id_sec = 924765620
    username_sec = "Severrrcompany"
    
    #Авторизация
    token = oauth(id, username)
    token_sec = oauth(id_sec, username_sec)
    
    #Тесты по ветке /users
    #users_get(token)
    #users_post(id, username)
    #users_delete(token)
    #users_put(token)
    #users_get_getreflink(token)
    #users_get_getref(token)
    #users_get_topleader(token)
    
    #Тесты по ветке /orders
    #orders_get(token)
    #orders_open_post(token)
    #orders_update_post(token)
    
    #Тесты по ветке /clans
    #clans_get(token)
    #clans_get_me(token)
    #clans_post(token)
    #clans_get_addmember(token_sec, -1001734381345)
    #clans_get_delmember(token_sec, -1001734381345)
    
    #Тесты по ветке /league
    #league_get(token)
    
