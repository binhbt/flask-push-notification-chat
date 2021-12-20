# flask-websocket-push-notification-and-chat  
Features:  
1. Flask websocket with redis broker for scale up on production  
2. Push notification on real time  
3. Group chat  
4. Read, unread, count user messages via rest apis  
5. Store messages by Mongo DB  
6. Test with wscat client  
### Deploy  
Run docker:  
>docker-compose up --build  
### Get session token  
>curl --location --request POST 'http://0.0.0.0:82/api/v1/notifications/generate_session_token' \  
>--header 'Content-Type: application/json' \  
>--data-raw '{"user_id":"111","device_id":"test_device", "role":"user", "model":"Xiaomi"}'  

Result  
>`{  
>    "token": "b1a69aa9-7b7d-4aa5-b2d3-4f8b7617f305"  
>}`  



### NOTIFICATIONS  
Run wscat connect to server as socket client  
Join 2 groups 111, 222  
>$wscat -c ws://0.0.0.0:82/ws/notification/b1a69aa9-7b7d-4aa5-b2d3-4f8b7617f305/111,222  
Join group 222  
>$wscat -c ws://0.0.0.0:82/ws/notification/b1a69aa9-7b7d-4aa5-b2d3-4f8b7617f305/222  
Join group 333  
>$wscat -c ws://0.0.0.0:82/ws/notification/b1a69aa9-7b7d-4aa5-b2d3-4f8b7617f305/333  

Push Message via rest api  
>`curl --location --request POST 'http://0.0.0.0:82/api/v1/notifications/push' \
>--header 'Content-Type: application/json' \
>--data-raw '{"group_ids":["111","333"], "message":"hello", "mtype":"type_a"}'`  
Client with id 111 will receive message  

### CHAT  
Join 2 groups 111, 222  
>$wscat -c ws://0.0.0.0:82/ws/chitchat/b1a69aa9-7b7d-4aa5-b2d3-4f8b7617f305/111,222  
Join group 222  
>$wscat -c ws://0.0.0.0:82/ws/chitchat/b1a69aa9-7b7d-4aa5-b2d3-4f8b7617f305/222  
Join group 333  
>$wscat -c ws://0.0.0.0:82/ws/chitchat/b1a69aa9-7b7d-4aa5-b2d3-4f8b7617f305/333  
Send message via wscat  
>${'from_id': '111', 'group_ids': ['111', '333'], 'message': 'hello1', 'mtype': 'chat_mess'}  

### APIS  
Read message  
`curl --location --request POST 'http://0.0.0.0:82/api/v1/notifications/messages/read' \  
--header 'Content-Type: application/json' \  
--data-raw '{"client_id":"111", "message_ids":["61af159d3b68f2c25c549bcd", "61af106418898f5b6bd23d7f"]}'`  

Delete messages  
>`curl --location --request DELETE 'http://0.0.0.0:82/api/v1/notifications/messages/del' \  
>--header 'Content-Type: application/json' \  
>--data-raw '{"client_id":"111", "message_ids":["61b87606abf665f1e802236e"]}'`  

Get list message  for client id 111 with groups 111 and 222  
>curl --location --request GET 'http://0.0.0.0:82/api/v1/notifications/111?group_ids=111,222&limit=10&offset=0'

Count total message for user 111 on group 111 and 222  
>curl --location --request GET 'http://0.0.0.0:82/api/v1/notifications/messages/111/count?group_ids=111,222'  
Result  
>`{
>    "read": 1,
>    "total": 12,
>    "unread": 11
>}`  


Have fun!
