$(function () {
    var csrftoken = getCookie('csrftoken');
    var toolbar = ['title', 'bold', 'italic', 'underline', 'strikethrough', 'color',
        '|', 'ol', 'ul', 'blockquote', 'table',
        '|', 'code', 'link', 'image', 'hr', 'emoji',
        '|', 'indent', 'outdent', 'markdown'];
    if ($('#id_content').length > 0) {
        $('#id_content').attr("data-autosave-confirm", "是否读取上次退出时未保存的草稿？");
        var editor = new Simditor({
            textarea: $("#id_content"),
            placeholder: "在此编辑你的文章",
            //optional options
            autosave: 'editor-content',
            markdown: true,
            toolbar: toolbar,
            emoji: {
                imagePath:  location.protocol + '//' + location.host + '/static/media/emoji/'
            },
            imageButton: ['upload', 'external'],
            defaultImage: location.protocol + '//' + location.host + '/static/media/image/simditor.png',
            upload: {
                url: '/upload/image/',
                params: {'csrfmiddlewaretoken': csrftoken,},
                fileKey: 'upload_image',
                connectionCount: 3,
                leaveConfirm: '正在上传，你确定要离开这个页面吗？',
            },
            codeLanguages: [
                {name: 'Python', value: 'python'},
                {name: 'Django', value: 'django'},
                {name: 'Shell', value: 'shell'},
                {name: 'Apache', value: 'apache'},
                {name: 'Java', value: 'java'},
                {name: 'CSS', value: 'css'},
                {name: 'JavaScript', value: 'javascript'},
                {name: 'HTML,XML', value: 'html'},
                {name: 'No Highlight', value: 'nohighlight'},
                {name: 'Diff', value: 'diff'},
                {name: 'SQL', value: 'sql'},
                {name: 'C++', value: 'c++'},
                {name: 'C#', value: 'cs'},
                {name: 'JSON', value: 'json'},
                {name: 'Markdown', value: 'markdown'},
            ]
        });
        $(".simditor").css({ "max-width": "930px", "overflow": "auto" });
    }
});