#-*-coding:utf-8-*-
from django.http import HttpResponse

import datetime

from django.views.generic import *
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from news.models import Article
from django.utils import timezone
from django.http import *

#coding:utf-8
from django.http import *
#from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt 
from time import gmtime, strftime
from django.shortcuts import render, render_to_response
from django.views.generic import *
from urlparse import urlparse
from django.core.paginator import Paginator
import datetime
from django.utils.timezone import utc
import base64

from testapp.models import *

class MyView(TemplateView):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')

def hello(request):
    return HttpResponse("Hello world")

def hi(request):
    return HttpResponse("Hi!")

def time(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404()
    dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
    html = "<html><body>In %s hour(s), it will be %s.</body></html>" % (offset, dt)
    return HttpResponse(html)

class ArticleCounterRedirectView(RedirectView):

    permanent = False
    query_string = True

    def get_redirect_url(self, pk):
        article = get_object_or_404(Article, pk=pk)
        article.update_counter()
        return reverse('product_detail', args=(pk,))
'''
class CommentCreateView(CreateView):
    model = Comment
    template_name = 'testapp/comment_create_view.html'
    
    def get_success_url(self):
        return reverse('comment_list')

    def get_context_data(self, **kwargs):
        kwargs["object_list"] = Comment.objects.all()
        return super(CommentCreateView, self).get_context_data(**kwargs)

class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'testapp/comment_update_view.html'

class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        """
        Redirect to the page listing all of the proxy urls
        """
        return reverse('comment_detail')

    def get(self, *args, **kwargs):
        """
        This has been overriden because by default
        DeleteView doesn't work with GET requests
        """
        return self.delete(*args, **kwargs)

#DetailView: design to display data
class CommentDetailView(DetailView):
    model = Comment
    template_name = 'testapp/comment_detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(CommentDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
'''

def get_comment_board(request, refer_url):
    #if specified page
    req_page = request.GET.get('page', None)
    if req_page is None or req_page is '':
        req_page = 1

    COMMENT_PER_PAGE = 5
    end_comment = (-req_page)*COMMENT_PER_PAGE
    start_comment = (1-req_page)*COMMENT_PER_PAGE
    if start_comment is 0:
        start_comment = None
    
    if refer_url is None:
        msgboard = messageBoard
    else:
        msgboard = msgboards.get(refer_url)
        if msgboard is None:
            #FIXME invalid case
            pass
    
    #获得最后COMMENT_PER_PAGE条
    to_show_messages = reversed(msgboard[end_comment:start_comment])
    #如果多余COMMENT_PER_PAGE条，翻页
    page_count = len(msgboard) / COMMENT_PER_PAGE + 1
    
    html = '<ul class="list-group">'
    #html = "<html><body>"
    for message in to_show_messages:
        #TODO 账户控制
        html += '<li class="list-group-item">'
        html += '<strong>路人甲</strong> '
        for ele in message:
            html += ele.encode('utf8') + ' '
        html += '<br>'#<hr/>
        html += '</li>'
    
    #如果不足 COMMENT_PER_PAGE ，则补齐
    if len(msgboard) < COMMENT_PER_PAGE:
        for i in range(COMMENT_PER_PAGE - len(msgboard)):
            html += '<li class="list-group-item">'
            html += '<br><br>'
            html += '</li>'
        
    html += '</ul>'
    
    html += '<div><ul class="pagination">'
    html += '<li><a href="#">«</a></li>'
    for i in range(1, page_count + 1):
        #onclick page load
        html += '<li><a href="#">'
        html += str(i)
        html += '</a></li>'
    html += '<li><a href="#">»</a></li>'
    html += '</ul></div>'

    #html += "</body></html>"
    return html

def length_not_enough(request):
    html = "<html><body>length not enough</body></html>"
    return html

class TestAppView(TemplateView):

    #用于测试request，args，kwargs
    def get(self, request, *args, **kwargs):
        print '----------request--------------'
        print request
        print '----------args--------------'
        print args
        print '----------kwargs--------------'
        print kwargs
        return HttpResponse('woca')

    def post(self):
        pass

'''
#每个URL单独一个CommentBoard
class CommentBoardView(TemplateView):
    count = 0
    def __init__(self, url):
        pass
    def get(self, request, *args, **kwargs):
        pass
    def post(self, request, *args, **kwargs):
        c = Comment(title="test-title", content="test-content")
        c.save()
        pass
    def delete(self, request, *args, **kwargs):
        pass
    def put(self, request, *args, **kwargs):
        pass
    def get_context_data(self, **kwargs):
        context = super(CommentBoardView, self).get_context_data(**kwargs)
        context['latest_articles'] = Comment.objects.all()[:5]
        return context

#ListView: Represent a list of objects
class CommentListView(ListView):
    model = Comment
    context_object_name = 'latest_comment_list'
    template_name = 'comments/comment_list_view.html'

#     def get_context_data(self, **kwargs):
#         context = super(CommentListView, self).get_context_data(**kwargs)
#         return context
'''
    
def leave_comment(comment_str, index_url):
    #len(messageBoard), 
    
    comment_tuple = [strftime("%Y-%m-%d %H:%M:%S", gmtime()), comment_str]
    messageBoard.append(comment_tuple)

    msgboards[index_url] = msgboards.get(index_url, [])
    msgboards[index_url].append(comment_tuple)
    
def write_comment_board(request, refer_url):
    comment = request.POST.get('comment', 'Empty Comment')
    leave_comment(comment, refer_url)

    return comment

def get_comment_board_template(request, refer_url):
    req_page = request.GET.get('page', None)
    if req_page is None or req_page is '':
        req_page = 1

    COMMENT_PER_PAGE = 5
    end_comment = (-req_page)*COMMENT_PER_PAGE
    start_comment = (1-req_page)*COMMENT_PER_PAGE
    if start_comment is 0:
        start_comment = None
    
    if refer_url is None:
        msgboard = messageBoard
    else:
        msgboard = msgboards.get(refer_url)
        if msgboard is None:
            #FIXME invalid case
            pass
    
    #获得最后COMMENT_PER_PAGE条
    to_show_messages = reversed(msgboard[end_comment:start_comment])
    #如果多余COMMENT_PER_PAGE条，翻页
    page_count = len(msgboard) / COMMENT_PER_PAGE + 1
    
    #render html here
    template_name = "comments/comment_board_get.html"
    return render(request, template_name, {
        'messages': to_show_messages,
        'n_messages': len(msgboard),
        'message_per_page': COMMENT_PER_PAGE,
        'refer_url': refer_url,
        'n_page': page_count + 1,
    })

def debug_comment(refer_url, netloc):
    return leave_comment(refer_url, netloc)

@csrf_exempt 
def comment_board(request, refer_url_b64 = None):
    '''
    主要程序入口，读取URL中的BASE64字符串并打印到board上，并解析POST/GET的参数，
    进行相应的动作。
    '''
    #不管是否是post，都先解析字符串，把refer_url打到comment里
    if refer_url_b64:
        refer_url = base64.b64decode(refer_url_b64)
        netloc = urlparse(refer_url).netloc
        debug_comment(refer_url, netloc)
    #如果是POST，那么写comment_board
    if request.method == 'POST':
        write_comment_board(request, netloc)
    #然后返回新的HTML，刷新掉老的。这里用jquery动态加载回复。
    res = HttpResponse(get_comment_board_template(request, netloc))
    res['Access-Control-Allow-Origin'] = '*'
    return res

msgboards = {}    #区分URL的msgboards
messageBoard = [] #只有一个的全局messageBoard
cursor = 0
    
msgboards = {}    #区分URL的msgboards
messageBoard = [] #只有一个的全局messageBoard
cursor = 0