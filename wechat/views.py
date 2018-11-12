from django.shortcuts import render

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import UserSerializer, GroupSerializer
import hashlib
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pythonweb.settings import conf
from lxml import etree
import time
from django.shortcuts import get_object_or_404, render


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

@csrf_exempt
def wechat_main(request):
    if request.method == "GET":
        # 接收微信服务器get请求发过来的参数
        signature = request.GET.get('signature', None)
        timestamp = request.GET.get('timestamp', None)
        nonce = request.GET.get('nonce', None)
        echostr = request.GET.get('echostr', None)
        # 服务器配置中的token
        token = conf.get('global', 'wechat_token')
        # 把参数放到list中排序后合成一个字符串，再用sha1加密得到新的字符串与微信发来的signature对比，如果相同就返回echostr给服务器，校验通过
        hashlist = [token, timestamp, nonce]
        hashlist.sort()
        hashstr = ''.join([s for s in hashlist]).encode('utf-8')
        hashstr = hashlib.sha1(hashstr).hexdigest()
        if hashstr == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("")
    else:
        # 这里是根据公众号中收到的消息（/关键词）去返回相关的资源信息，使用文本消息接口
        print('收到消息={}'.format(request.body))
        str_xml = etree.fromstring(request.body)
        msg_type = str_xml.find('MsgType').text
        if msg_type == 'text':
            fromUser = str_xml.find('ToUserName').text
            toUser = str_xml.find('FromUserName').text
            content = str_xml.find('Content').text
            nowtime = str(int(time.time()))

            # 用模板构建返回给微信的数据
            c = {'toUser': toUser, 'fromUser': fromUser, 'nowtime': nowtime, 'content': content}
            return render(request, 'wechat/text.xml', c)
        else:
            print("暂不处理")
            return HttpResponse("success")


def autoreply(request):
    pass

