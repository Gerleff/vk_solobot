"""
:authors: gerleffx2
:license:
:copyright: (c) 2019 gerleffx2
"""
import vk_api

token = '41eb831dae59397e81f9d3ab9365ef99108e840463393f75d1a356cde683c8c87e17ae13379294201b55e'
group_id = '112199313'


def main():
    vk = vk_api.VkApi(token=token).get_api()
    print(vk.messages.getConversations(group=group_id, count=1))
    count = vk.messages.getConversations(group=group_id, count=1)['count']
    files_amount = int(count) // 1000 + 1
    for j in range(files_amount):
        with open('/parse/'+str(j)+'.txt', 'w') as f:
            try:
                for i in range(1000):
                    id_user = \
                        vk.messages.getConversations(group=group_id, offset=i+j*1000, count=1)['items'][0]['conversation']['peer']['id']
                    f.write(id_user+"\n")
            except:
                f.close()
                continue
        f.close()


if __name__ == '__main__':
    main()
