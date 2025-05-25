import requests as re
from io import BytesIO

def file_senders(e6_client, command, args):

    # modify tags
    if command in ['e6', 'bomb']:
        tags = args.split(' ')
    else:
        tags = []

    # modify number of images
    if command in ['bomb']:
        number = 10
    else:
        number = 1
        
    # Choose full size or sample
    if command in ['bomb']:
        full_size = False
    else:
        full_size = True
        
    images = [image for image in e6_client.random_images(tags, number=number, full_size=full_size) if image['url'] is not None]

    image_files = []

    for image in images:
        if image['name'].split('.')[-1] not in ['swf', 'webm']:
            image_files.append(download_file(image['url'], image['name']))

    return image_files


def download_file(url, file_name):

    data = re.get(url).content

    file = BytesIO()
    file.write(data)
    file.seek(0)

    file.name = file_name

    return file