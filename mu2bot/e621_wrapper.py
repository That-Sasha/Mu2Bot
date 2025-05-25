import requests as re

class E621:

    def __init__(self, blacklist=[], default_order=None):
        # blacklist : str array
        # default_order : str 
        #   - random, favcount, etc.

        self.blacklist = blacklist
        self.default_order = default_order

        # Base url for most use cases
        self.endpoint = lambda action : f'https://e621.net/{action}.json'
        self.user_agent = 'e621_api_wrapper'

        self.default_headers = {
            'user-agent' : self.user_agent
        }


    def list_posts(self, tags, order=None, limit=50, page=1):
        # tags : str array

        tag_str = '+'.join(tags)

        if order is None:
            order = self.default_order

        parameters = {
            'tags' : f'order:{order}+{"+".join(tags + self.blacklist)}',
            'limit' : limit,
            'page' : page
        }

        payload_str = "&".join(f'{k}={v}' for k,v in parameters.items() if v is not None )

        response = re.get(
            self.endpoint('posts'), 
            params=payload_str, 
            headers=self.default_headers
        )

        return response.json()

    def random_images(self, tags, number=1, full_size=True):

        posts = self.list_posts(tags, order='random', limit=number, page=None)['posts']
        if len(posts) == 0:
            return False

        images = []

        for post in posts:
            file = post['file']
            sample = post['sample']
            
            if full_size and sample['has'] == 'true':
                url = sample['url']
            else:
                url = file['url']


            images.append({
                'url' : url,
                'name' : f"{file['md5']}.{file['ext']}"
            })

        return images

        






