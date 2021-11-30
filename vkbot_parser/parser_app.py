from vkbot_parser.vk_parser import AlbumsParser

app = AlbumsParser()

if __name__ == '__main__':
    photos = app.get_photos('esg')
    print(app.get_comments('esg', all_photos=photos))
