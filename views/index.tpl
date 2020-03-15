<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>首页</title>
</head>
<body>
    Welcome！
    <hr>
    <table border="1">
        <tr>
            <th>序号</th>
            <th>标题</th>
            <th>作者</th>
            <th>发表时间</th>
        </tr>
        % for k, v in posts_data.items():
        <tr>
            <td>{{ k }}</td>
            <td><a href="/post/show/{{v['slug']}}">{{ v['title'] }}</a></td>
            <td>{{ v['author'] }}</td>
            <td>{{ v['ctime'] }}</td>
        </tr>
        % end
    </table>
    <div class="pages">
        <a href="/?page={{page-1}}">上一页</a>
        <a href="">{{page}}</a>
        <a href="/?page={{page+1}}">下一页</a>
    </div>
    <a href="/post/new">发布文章</a>
</body>
</html>