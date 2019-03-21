#!usr/bin/env python
# -*- coding: utf-8 -*-
# *******************************************************
# @File:     upload
# @Auth:     winver9@gmail.com
# @Create:   2019-2-26 14:47
# @License:  © Copyright 2019, LBlog Programs.
# *******************************************************
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.conf import settings
from PIL import Image, ImageSequence

import os, uuid

def compresImage(image):
    width = image.width
    height = image.height
    rate = 1.0  # 压缩率
    # 根据图像大小设置压缩率
    if width >= 2000 or height >= 2000:
        rate = 0.3
    elif width >= 1000 or height >= 1000:
        rate = 0.5
    elif width >= 500 or height >= 500:
        rate = 0.9
    width = int(width * rate)  # 新的宽
    height = int(height * rate)  # 新的高
    # 生成缩略图
    image.thumbnail((width, height), Image.ANTIALIAS)
    return image

def uploadImage(request):
    if request.method == 'POST':
        file = request.FILES['upload_image']
        if file.size > 500000:
            return JsonResponse({
                'success': False,
                'file_path': '',
                'msg': '上传的图片大小不能超过500K'
            })
        if file.name.split('.')[-1] in ['jpg', 'jpeg', 'png', 'bmp', 'gif']:
            #这里的file_path指的是服务器上保存图片的路径
            image = Image.open(file)
            file_path = settings.MEDIA_IMAGE_ROOT + uuid.uuid4().hex + '.' + image.tile[0][0]
            # GIF单独保存
            #print(image.tile, image.tile[0][0], image.size, image.height, image.width)
            if image.tile[0][0] == 'gif':
                frames = [frame.copy() for frame in ImageSequence.Iterator(image)]
                print(frames)
                print(type(image))
                image.save(file_path, save_all=True, append_images=frames)
                return JsonResponse({
                    'success': True,
                    # 这里的file_path指的是访问该图片的url
                    'file_path': settings.MEDIA_URL + 'image/' + os.path.basename(file_path),
                    'msg': 'Success!'
                })
            try:
                r, g, b, a = image.split()
                image = Image.merge('RGB', (r, g, b))
            except:
                pass
            image = compresImage(image)
            image.save(file_path)
            return JsonResponse({
                'success': True,
                #这里的file_path指的是访问该图片的url
                'file_path': settings.MEDIA_URL + 'image/' + os.path.basename(file_path),
                'msg': 'Success!'
                })
        else:
            return JsonResponse({
                'success': False,
                'file_path': '',
                'msg': 'Unexpected File Format!'
                })
    else:
        raise PermissionDenied('Only Accept POST Request!')