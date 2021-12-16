from models.models import NotiMessage, UserReadMessage, UserDeleteMessage

def save_new_message(data):
    message = NotiMessage(**data)
    message.status="publish"
    message.save()

def update_message_status(id, status):
    message = NotiMessage.objects(id=id).first()
    if not message:
        return False
    else:
        message.update(status=status)
    return message
def get_message_send_from_id(from_id, group_ids, status=None,limit=10, offset=0):
    group_ids = get_group_ids(group_ids)

    messages = NotiMessage.objects.filter(group_ids__in=group_ids).filter(from_id=from_id)
    if status:
        messages = messages.filter(status=status)
    messages = messages.limit(int(limit)).skip(int(offset)).all()

    return messages
def get_message_by_group_ids(client_id, group_ids, status=None,limit=10, offset=0):
    group_ids = get_group_ids(group_ids)

    # print(group_ids)
    # print(status)
    # print(limit)
    messages = NotiMessage.objects.filter(group_ids__in=group_ids)
    if status:
        messages = messages.filter(status=status)
    messages = messages.limit(limit).skip(offset).all()

    ids =[str(message.id) for message in messages]
    print(ids)
    read_messages = UserReadMessage.objects.filter(message_id__in=ids).filter(client_id=client_id).all()
    read_ids =None
    if read_messages:
        read_ids=[str(read.message_id) for read in read_messages]
    print(read_messages)
    rs =[]
    for msg in messages:
        jsonObj = msg.to_json()
        is_read = False
        if read_ids and str(msg.id) in read_ids:
            is_read = True
        jsonObj['is_read'] = is_read
        rs.append(jsonObj)

    return rs
def get_message_by_group_ids1(client_id, group_ids, status=None,limit=10, offset=0):
    group_ids = get_group_ids(group_ids)
    if not limit:
        limit =10
    if not offset:
        offset = 0
    # print(group_ids)
    # print(status)
    # print(limit)
    pipeline = [
        {"$sort" : {"created" : -1}},
        {"$skip": int(offset) },
        {"$limit": int(limit) },
        {"$addFields": {"message_id": { "$toString": "$_id"}}},
        {"$match": {"group_ids": {"$in":group_ids}}},
        {       "$lookup":
                {
                    "from": "user_read_message",
                    "localField": "message_id",
                    "foreignField": "message_ids",
                    # "let": { "message_ids": "$message_ids" },
                    "as": "read",
                    "pipeline": [
                        # {"$match": {"message_id": {"$in":"$$message_ids"}}},
                        { "$match": {"client_id": {"$eq":client_id}}}
                        ],
                }
        },
        {       "$lookup":
                {
                    "from": "user_delete_message",
                    "localField": "message_id",
                    "foreignField": "message_ids",
                    "as": "del",
                    "pipeline": [
                        { "$match": {"client_id": {"$eq":client_id}}}
                        ],
                }
        },
        {"$match": {"del": {"$exists": True, "$type": "array", "$eq": [] }}}, 
    ]
    if status:
        cond ={ "$match": {"status": {"$eq":status}}}
        pipeline.append(cond)

    messages= NotiMessage.objects().aggregate(pipeline)
    # print(messages)
    rs =[]
    for jdata in messages:
        jdata['_id']=str(jdata['_id'])
        if jdata['read']:
            jdata['read'] = True
        else:
            jdata['read'] = False
        rs.append(jdata)
    print(rs)
    return rs

def read_message(data):
    message = UserReadMessage.objects(client_id=data['client_id'], message_ids__in=data['message_ids']).first()
    if not message:
        message = UserReadMessage(**data)
        message.save()
        return message.to_json()
    else:
        # message = UserReadMessage(**data)
        # message.save()
        return {'message':'Invalid data'}
def del_message(data):
    message = UserDeleteMessage.objects(client_id=data['client_id'], message_ids__in=data['message_ids']).first()
    if not message:
        message = UserDeleteMessage(**data)
        message.save()
        return message.to_json()
    else:
        # message = UserDeleteMessage(**data)
        # message.save()
        return {'message':'Invalid data'}

def count_message_by_group_ids(client_id, group_ids, status=None):
    group_ids = get_group_ids(group_ids)
    # print(status)
    pipeline = []
    if status:
        pipeline = [{ "$match": {"status": {"$eq":status}}}]
    pipeline.extend([
        {"$match": {"group_ids": {"$in":group_ids}}},
        {"$facet": {
            "Total": [
            {"$addFields": {"message_id": { "$toString": "$_id"}}},
            { "$lookup":
                        {
                            "from": "user_delete_message",
                            "localField": "message_id",
                            "foreignField": "message_ids",
                            "as": "del",
                            "pipeline": [
                                { "$match": {"client_id": {"$eq":client_id}}}
                                ],
                        }
            },
            {"$match": {"del": {"$exists": True, "$type": "array", "$eq": [] }}}, 
            { "$count": "Total" },
            ],
            "Read": [
            {"$addFields": {"message_id": { "$toString": "$_id"}}},
            { "$lookup":
                        {
                            "from": "user_read_message",
                            "localField": "message_id",
                            "foreignField": "message_ids",
                            "as": "read",
                            "pipeline": [
                                { "$match": {"client_id": {"$eq":client_id}}}
                                ],
                        }
            },
            
            {"$match": {"read": {"$exists": True, "$type": "array", "$ne": [] }}}, 
            
            { "$lookup":
                        {
                            "from": "user_delete_message",
                            "localField": "message_id",
                            "foreignField": "message_ids",
                            "as": "del",
                            "pipeline": [
                                { "$match": {"client_id": {"$eq":client_id}}}
                                ],
                        }
            },
            {"$match": {"del": {"$exists": True, "$type": "array", "$eq": [] }}}, 
            {"$count": "Total" }
            ],
            
        }},
        { "$project": {
            "total": { "$arrayElemAt": ["$Total.Total", 0] },
            "read": { "$arrayElemAt": ["$Read.Total", 0] },
            "unread": { "$subtract": [ { "$arrayElemAt": ["$Total.Total", 0] }, { "$arrayElemAt": ["$Read.Total", 0] } ] }
        }},
    ])
    print(pipeline)

    message= NotiMessage.objects.aggregate(pipeline)
    rs=[]
    for jdata in message:
        rs.append(jdata)
    print(rs)
    return rs[0]


def get_group_ids(params):
    if params:
        return params.split(',')
    return None
def is_have_message(params, msg):
    group_ids = get_group_ids(params)
    if group_ids:
        for group_id in group_ids:
            client1 ='"{}"'.format(group_id)
            client2 =client1.replace('"',"'")
            print(client1)
            print(client2)
            if client1 in str(msg) or client2 in str(msg):
                return True
    return False

