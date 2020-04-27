var log = console.log.bind(console, new Date().toLocaleString())

var e = function (selector) {
    return document.querySelector(selector)
}

var messageTemplate = function (message_author, message_content) {
    var t = `
    <div class="message-cell">
        <span>${message_author} 说：${message_content} </span>
    </div>
    `

    return t
}

/*
1. 给 add button 绑定事件
2. 在事件处理函数中，获取 input 的值
3. 用获取的值，组装一个 message-cell HTML 字符串
4. 插入 message-list 中
*/

var insertMessage = function (messageCell) {
    var form = document.querySelector('#id-message-list')
    form.insertAdjacentHTML('beforeend', messageCell)
}

var loadMessages = function () {
    ajax('POST', '/message/show', {}, function (json) {
        log('拿到ajax响应')
        log('response data', json)
        for (var i = 0; i < json.length; i++) {
            log('json for', json[i], json)
            var message_author = json[i].username
            var message_content = json[i].content
            var messageCell = messageTemplate(message_author, message_content)
            log(messageCell)
            insertMessage(messageCell)
        }
    })
}

var bindEvents = function () {
    var b = e('#id-button-add')
    b.addEventListener('click', function () {
        log('click')
        var input = e('#id-input-message')
        log(input)
        log(input.value)
        var message_content = input.value
        var author_name = e('#id-author-username')
        var author = author_name.value
        var messageCell = messageTemplate(author, message_content)
        log(messageCell)

        var data = {
            content: message_content
        }
        ajax('POST', '/message/add', data, function (json) {
            log('拿到ajax响应')
            var message = json.message
            alert(message)
            insertMessage(messageCell)
        })
    })
}

var main = function () {
    loadMessages()
    bindEvents()
}

main()