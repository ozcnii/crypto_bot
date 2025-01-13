if __name__ == "__main__":
    import requests
    from config import DevelopmentConfig
    import json
    
    def user_get_test():
        return\
            requests.get(f"{DevelopmentConfig.HOST}/users").json()
    def clan_get_test():
        return\
            requests.get(f"{DevelopmentConfig.HOST}/clans").json()
    def clan_getOne_test():
        return\
            requests.get(f"{DevelopmentConfig.HOST}/clans/get/0").json()
    def clans_add_test():
        return\
            requests.get(f"{DevelopmentConfig.HOST}/clans/addmember/0/3").json()
    def clans_del_test():
        return\
            requests.get(f"{DevelopmentConfig.HOST}/clans/delmember/0/3").json()
    def boosters_get_test():
        return\
            requests.get(f"{DevelopmentConfig.HOST}/boosters").json()
    def boosters_upgrade_test():
        return\
            requests.get(f"{DevelopmentConfig.HOST}/boosters/upgrade/leverage/2").json()
    def boosters_activate_test():
        return\
            requests.get(f"{DevelopmentConfig.HOST}/boosters/activate/xrange/2").json()
    def boosters_deactivate_test():
        return\
            requests.get(f"{DevelopmentConfig.HOST}/boosters/deactivate/xrange/2").json()
    def orders_get_test():
        return\
            requests.get(f"{DevelopmentConfig.HOST}/orders").json()
    def stories_get_test():
        return\
            requests.get(f"{DevelopmentConfig.HOST}/stories").json()
    def stories_search_get_test():
        return\
            requests.get(f"{DevelopmentConfig.HOST}/stories/1").json()
    def userSearch_get_test():
        return\
            requests.get(f"{DevelopmentConfig.HOST}/users/2").json()
    def user_getreflink_test():
        return\
            requests.get(f"{DevelopmentConfig.HOST}/users/0/getreflink").json()
    def user_post_test():
        return\
            requests.post(
                f"{DevelopmentConfig.HOST}/users",
                headers={
                    'Content-Type': 'application/json'
                },
                data=json.dumps({
                    "chat_id":3,
                    "username":"admin1",
                    "balance":1000,
                    "league":"bronze",
                    "boosters":[0,0,0,0,0],
                })
            ).json()
            
    def clans_post_test():
        return\
            requests.post(
                f"{DevelopmentConfig.HOST}/clans",
                headers={
                    'Content-Type': 'application/json'
                },
                data=json.dumps({
                    "peer":0,
                    "admin":2,
                    "users":[2],
                    "league":"bronze",
                    "name":"test",
                })
            ).json()
    def clans_delete_test():
        return\
            requests.delete(
                f"{DevelopmentConfig.HOST}/clans",
                headers={
                    'Content-Type': 'application/json'
                },
                data=json.dumps({
                    "admin":2,
                    "peer":0
                })
            ).json()
    def clans_put_test():
        return\
            requests.put(
                f"{DevelopmentConfig.HOST}/clans",
                headers={
                    'Content-Type': 'application/json'
                },
                data=json.dumps({
                    "peer":0,
                    "admin":2,
                    "users":[2],
                    "league":"bronze",
                    "name":"testPut",
                })
            ).json()
    def user_put_test():
        return\
            requests.put(
                f"{DevelopmentConfig.HOST}/users/3",
                headers={
                    'Content-Type': 'application/json'
                },
                data=json.dumps({
                    "balance":1000,
                    "league":"bronze"
                })
            ).json()
            
    def user_delete_test():
        return\
            requests.delete(
                f"{DevelopmentConfig.HOST}/users",
                headers={
                    'Content-Type': 'application/json'
                },
                data=json.dumps({
                    "chat_id":1,
                })
            ).json()
            
    def user_orders_test():
        return\
            requests.post(
                f"{DevelopmentConfig.HOST}/orders/open/2",
                headers={
                    'Content-Type': 'application/json'
                },
                data=json.dumps({
                    "symbol":"TON",
                    "priceinput": 6.36,
                    "amount":100,
                    "position":"long",
                    "leverage":1
                })
            ).json()
            
    def user_orders_update_test():
        return\
            requests.post(
                f"{DevelopmentConfig.HOST}/orders/update/2",
                headers={
                    'Content-Type': 'application/json'
                },
                data=json.dumps({
                    "coinprice": 7.6,
                })
            ).json()
            
    #Регистрация пользователя
    # print(user_post_test())
    # print(user_put_test())
    # print(userSearch_get_test())
    
    #Ордеры
    # print(user_orders_test())
    # print(user_orders_update_test())

    #Бустеры
    # print(boosters_get_test())
    # print(boosters_upgrade_test())
    # print(boosters_activate_test())
    
    #Кланы
    # print(clan_get_test())
    # print(clan_getOne_test())
    # print(clans_post_test())
    # print(clans_put_test())
    # print(clans_del_test())
    # print(clans_add_test())
    print(clans_delete_test())