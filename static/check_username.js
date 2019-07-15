var log = console.log.bind(console, new Date().toLocaleString())

var e = function (selector) {
    return document.querySelector(selector)
}
// 包含所有字母的字符串alpha
var alpha =
    'abcdefghijklmnopqrstuvwxyz' +
    'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
// 包含所有数字字符的字符串num
var num = '0123456789'

var bindEvents = function () {
    // 选择器查找按钮
    var b = e('#id-button-login')
    b.addEventListener('click', function () {
        // 选择器查找输入框，获取输入的用户名
        var input = e('#id-input-username')
        var username = input.value
        var length = username.length
        // 布尔变量flag来记录是否合法
        var flag = false
        // 判断长度是否大于等于2；判断第一个字符是否是字母
        if (length >= 2 && alpha.indexOf(username[0]) !== -1) {
            // 判断结尾是否是数字或字母
            if (alpha.indexOf(username[length - 1]) !== -1 || num.indexOf(username[length - 1]) !== -1) {
                // 判断是否超过最大长度
                if (length <= 10) {
                    for (var i = 1; i < length - 1; i++) {
                        // 循环遍历username，判断首尾之外的字符是否只包含字母、数字、下划线
                        if (alpha.indexOf(username[i]) === -1 && num.indexOf(username[i]) === -1 && username[i] !== '_') {
                            // 若不是，则将flag设为false，跳出循环
                            flag = false
                            break
                        }
                    }
                    // i == length-1 说明循环完了所有中间字符，都是合法的
                    if (i === length - 1) {
                        flag = true
                    }
                }
            }
        }
        // 选择该h3元素
        var result = e('#id-username-result')
        var check = e('#check-username')
        if (flag === true) {
            log('检查合格')
            result.innerText = '【检查合格】'
            check.value = 'valid'
        } else {
            log('用户名错误')
            result.innerText = '【不合格的用户名】'
            check.value = 'invalid'
        }
    })
}

var main = function () {
    bindEvents()
}

main()