from bottle import route, run, template, view, request, redirect, abort
import redis
import time
import json

r = redis.StrictRedis()

@route('/')
@view('index')
def index():
    page = request.query.page or '1'
    page = int(page)

    posts_per_page = 10
    start = (page - 1) * posts_per_page
    end = page * posts_per_page - 1

    posts_id_bytes = r.lrange('posts:list', start, end)
    posts_id = [id.decode('utf-8') for id in posts_id_bytes]
    
    posts_data = {}
    for id in posts_id:
        post_data_bytes = r.hgetall('post:{}'.format(id))
        post_data = {k.decode('utf-8'):v.decode('utf-8') for k,v in post_data_bytes.items()}
        posts_data[id] = post_data
    return dict(posts_data=posts_data, page=page)

@route('/post/new')
@view('newpost')
def post_new():
    return dict()

@route('/post/deal', method='POST')
@view('newpost')
def post_deal():
    postid = r.incr("posts:count")

    title = request.forms.getunicode('title')
    content = request.forms.getunicode('content')
    author = request.forms.getunicode('author')
    slug = request.forms.getunicode('slug')
    ctime =  time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))

    is_slug_available = r.hsetnx('slug.to.id', slug, postid)
    if not is_slug_available:
        return dict(tips = '缩略词已经存在，请更换')

    post_data = {
        'title' : title,
        'content' : content,
        'author' : author,
        'slug' : slug,
        'ctime' : ctime
    }

    r.hmset('post:{}'.format(postid), post_data)
    r.lpush('posts:list', postid)
    redirect('/post/show/{}'.format(slug))

@route('/post/show/<slug>')
@view('showpost')
def post_show(slug):
    id = r.hget('slug.to.id', slug)
    if not id:
        abort(404, '文章不存在!')

    id = id.decode('utf-8')

    visit_times = r.incr('post:{}:visited'.format(id))
    post_data_bytes = r.hgetall('post:{}'.format(id))
    post_data = {k.decode('utf-8'):v.decode('utf-8') for k,v in post_data_bytes.items()}
    
    post_tags_bytes = r.smembers('post:{}:tags'.format(id))
    post_tags = {tag.decode('utf-8') for tag in post_tags_bytes}
    return dict(post_data = post_data, visit_times = visit_times, post_id = id, post_tags = post_tags)

@route('/post/addtags', method='POST')
def tag_add():
    post_id = request.forms.getunicode('id')
    tag = request.forms.getunicode('tag')

    r.sadd('post:{}:tags'.format(post_id), tag)
    r.sadd('tag:{}:post'.format(tag), post_id)
    return dict()


run(host='localhost', reloader=True, port=8080)