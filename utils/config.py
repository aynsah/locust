class SharedData(object):
    token = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdXRob3JpemVkIjp0cnVlLCJkb21haW4iOiJhbGxpbm9sc2VyYTIiLCJkdGlkIjoiYjJiYTA2MDVlY2U1MGExMjcxMDBkNjY1ZTkxYjI4MzRjZWRhYWViYzdkYmMwMDVmOTUyZTZlMjU5ZWU2MDhlZTU0MTMwZTRmNjQwYjUwNDc2ZWI0MGFjZDEyMTdjMDBiMzU1YjRjM2IxZmU3ZTdhNjU4Y2UwMWZiZWEzZjdlY2MiLCJleHBpYXJ5X3RpbWUiOiIyMDIyLTA3LTI5VDA4OjQ0OjQ3Ljk4MjUwOTYrMDc6MDAiLCJ1c2VyX2lkIjpudWxsfQ.FIZ6rd5jHBgVg2GZVvpzxHxcpbVkKp-VPsZ8X-OqLUo"
    lang = "en"
    domain = "allinolsera2"
    client = {"client_id": 1, "client_secret":"2"}
    base_url = "/" + lang + "/" + domain
    user_id = 0
    users = [
        {"phone":"+6289636916356", "password":"sadness"}
    ]
    now = ""
    cart_token = ""

def base_url():
    return "/" + SharedData.lang + "/" + SharedData.domain