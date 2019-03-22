//全局变量
var commentOuter = $('#comment-outer')[0];
var commentCancel = $('#comment-cancel')[0];
var commentSave = $('#comment-save')[0];

//Ajax提交评论
function commentStart() {
    var articleContent = $('#id_content')[0].value;
    var articleId = $('#id_article')[0].value;
    var csrftoken = getCookie('csrftoken');

    if (articleContent !== '') {
        $.ajax({
            url: location.href + '/comment/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                "content": articleContent,
                "articleId": articleId,
                "userId": 1,
            }),
            dataType: 'json',
            headers: {'X-CSRFToken': csrftoken},
            success: function () {
                $('#id_content')[0].value = '';
                alert('评论成功，将于24小时内审核通过~');
            }
        })
    }
}

//Ajax删除评论
function commentDelete(commentId) {
    if (confirm('确认删除？')) {
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: location.href + '/comment/',
            type: 'DELETE',
            data: JSON.stringify({
                "commentId": commentId
            }),
            dataType: 'json',
            headers: {'X-CSRFToken': csrftoken},
            success: function (data) {
                $.get(location.href, function () {
                    location.reload();
                });
                alert(data.msg)
            }
        })
    } else {
        return false;
    }
}

//Ajax回复评论
function commentReply(commentUser, commentId, replyCommentId) {
    commentOuter.style.display = 'block';
    $('#comment-re')[0].innerText = '┗回复：'+commentUser;
    var articleId = $('#comment-form>input[name=article]')[0].value;
    var csrftoken = getCookie('csrftoken');

    commentSave.onclick = function () {
        var replyContent = $('#comment-form>textarea[name=content]')[0].value;
        if (replyContent !== '') {
            console.log(replyContent);
            $.ajax({
                url: location.href + '/reply/',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({
                    'commentId': commentId,
                    'replyCommentId': replyCommentId,
                    'replyContent': replyContent,
                }),
                dataType: 'json',
                headers: {'X-CSRFToken': csrftoken},
                success: function () {
                    replyContent = '';
                    alert('回复成功，将于24小时内审核通过~');
                    commentOuter.style.display = 'none';
                }
            });
        }
    };

    commentCancel.onclick = function () {
        $('#comment-form>textarea')[0].value = '';
        commentOuter.style.display = 'none';
    };
}

//Ajax删除回复
function commentReplyDelete(commentReplyId) {
    if (confirm('确认删除？')) {
        var csrftoken = getCookie('csrftoken');
        $.ajax({
            url: location.href + '/reply/',
            type: 'DELETE',
            data: JSON.stringify({
                "replyId": commentReplyId
            }),
            dataType: 'json',
            headers: {'X-CSRFToken': csrftoken},
            success: function (data) {
                $.get(location.href, function () {
                    location.reload();
                });
                alert(data.msg)
            }
        })
    } else {
        return false;
    }
}



/*
 ajax提交评论
 */
/*
var commentSave = $('#comment-save')[0];
commentSave.onclick = function () {
    var articleContent = $('#id_content')[0].value;
    var articleId = $('#id_article')[0].value;
    var csrftoken = getCookie('csrftoken');
    $.ajax({
        url: '/article/'+articleId,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            "content": articleContent,
        }),
        dataType: 'json',
        headers: {'X-CSRFToken': csrftoken},
        success: function (data) {
            var commentList = document.getElementById('comment-list');
            innerHtml = document.createElement('li');
            console.log(data);
            innerHtml.innerText = data.content;
            commentList.appendChild(innerHtml);
            commentOuter.style.display = 'none';
        }
    })
}
*/