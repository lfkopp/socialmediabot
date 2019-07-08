def get_credentials(socialmedia):
    with open('credentials.txt', 'r') as file:
        credentials = eval(str(file.read()))
    return credentials[socialmedia]['user'], credentials[socialmedia]['password']

def get_shortcode(hashtag='internetofthings',num=5):
    import requests
    import json

    lista = []
    content = requests.get('https://www.instagram.com/explore/tags/'+str(hashtag)+'/?__a=1').text
    a = json.loads(str(content))
    for i in range(num):
        try:
            for b in a['graphql']['hashtag']['edge_hashtag_to_media']['edges']:
                code = b['node']['shortcode']
                if code not in lista:
                    link = 'https://www.instagram.com/p/'+code
                    lista.append(str(link))
            #print(lista)
            end_cursor = a['graphql']['hashtag']['edge_hashtag_to_media']['page_info']['end_cursor']
            content = requests.get('https://www.instagram.com/explore/tags/'+str(hashtag)+'/?__a=1&max_id='+str(end_cursor)).text
            a = json.loads(str(content))
        except Exception as e:
            print(e)
            return lista
    return lista
