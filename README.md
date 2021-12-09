# flask-websocket-push-notification-mongo
Run docker: docker-compose up --build  
Run wscat connect to server as socket client  
Join 2 groups 111, 222  
wscat -c ws://167.71.218.57/ws/notification/111#222  
Join group 222  
wscat -c ws://0.0.0.0:82/echo/222  
Join group 333  
wscat -c ws://0.0.0.0:82/echo/333  
Push Message via rest api  
`curl --location --request POST 'http://0.0.0.0:82/api/v1/notifications/push' \
--header 'Content-Type: application/json' \
--data-raw '{"group_ids":["111","333"], "message":"hello", "mtype":"provider_noti"}'`  
Client with id 111 will receive message  

Get list message  for client id 111 with groups 111 and 222  
curl --location --request GET 'http://0.0.0.0:82/api/v1/notifications/111?group_ids=111,222&status=unread&limit=10&offset=0'

Count total message for user 111 on group 111 and 222  
curl --location --request GET 'http://0.0.0.0:82/api/v1/notifications/messages/111/count?status=unread&group_ids=111,222'  
Result  
`{
    "read": 1,
    "total": 12,
    "unread": 11
}`  


Have fun!
