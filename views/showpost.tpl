<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>文章</title>
    <script src="https://cdn.bootcss.com/jquery/3.4.1/jquery.min.js"></script>
    <style>
        .post-tag {
            margin-right: 20px;
        }
    </style>
</head>
<body>
ID:

<span id="post-id">{{ post_id }}</span>

<br>

标题:

{{ post_data['title'] }}

<br>

内容:

{{ post_data['content'] }}

<br>


作者:

{{ post_data['author'] }}

<br>

发布时间:

{{ post_data['ctime'] }}

<br>

访问量:

{{ visit_times }}

<hr>

<h3>标签:</h3>
<div id="tags-list">
    % for tag in post_tags:
        <a class='post-tag' href="/tags/?tag={{tag}}">{{tag}}</a>
    % end
</div>

<div>
    <textarea name="tag" id="tag" cols="30" rows="10"></textarea>
    <br>
    <button onclick="addtag()">添加标签</button>    
</div>

<script>
    function addtag() {
        let tag = $("#tag").val()
        let post_id = $('#post-id').text()
        let data = {
            'id': post_id,
            "tag": tag
        }
        console.log(data)
        $.post("/post/addtags", data ,function(result){
            $("#tags-list").append(`<a class='post-tag' href='/tags/?tag=${tag}'>${tag}</a>`)
        });
    }
</script>
</body>
</html>