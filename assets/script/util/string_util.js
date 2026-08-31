/**
 * 字符串工具类
 */


/**
 * 判断字符串是否以指定字符串开始
 * @param  {String}     match   [起始字符串]
 * @return {Boolean}            [结果]
 */
String.prototype.startWith = function (match) {
    return this.slice(0, match.length) === match
}

/**
 * 判断字符串是否以指定字符串结束
 * @param  {String}     match   [结束字符串]
 * @return {Boolean}            [结果]
 */
String.prototype.endWith = function (match) {
    return this.slice(-match.length) === match
}

/**
 * 判断字符的类型
 * @return {String}   [结果] 
 * @enum {uppercase, lowercase, digit, bracketS, bracketE, symbol}
 */
String.prototype.charFormat = function () {
    if (/[0-9]/.test(this)) return "digit"
    if (/[A-Z]/.test(this)) return "uppercase"
    if (/[a-z]/.test(this)) return "lowercase"
    if (this == "(") return "bracketS"
    if (this == ")") return "bracketE"
    return "symbol"
}

/**
 * 判断字符长度
 * @return {number}   [结果] 
 */
String.prototype.utf8len = function () {
    var len = 0
    for (var i = 0; i < this.length; i++) {
        if (this.charCodeAt(i) > 127 || this.charCodeAt(i) == 94) {
            len += 2
        } else {
            len++
        }
    }
    return len
}

/**
 * 格式化字符串
 * @param {String} format 格式化定义
 */
String.prototype.format = function (...args) {
    var ret = this
    if (args.length > 0) {
        if (args instanceof Array) {
            for (var i = 0; i < args.length; i++) {
                if (args[i] != undefined) {
                    var reg = new RegExp("({)" + i + "(})", "g")
                    ret = ret.replace(reg, arguments[i])
                }
            }
        } else {
            for (var key in args) {
                if (args[key] != undefined) {
                    var reg = new RegExp("({" + key + "})", "g")
                    ret = ret.replace(reg, args[key])
                }
            }
        }
    }
    return ret
}

/**
 * 格式化日期字符串
 * @param  {string} format [格式化定义]
 * @return {string}        [指定格式日期字符串]
 */
Date.prototype.format = function (format) {
    var date = {
        "M+": this.getMonth() + 1,
        "d+": this.getDate(),
        "h+": this.getHours(),
        "m+": this.getMinutes(),
        "s+": this.getSeconds(),
        "q+": Math.floor((this.getMonth() + 3) / 3),
        "S+": this.getMilliseconds()
    };
    if (/(y+)/i.test(format)) {
        format = format.replace(RegExp.$1, (this.getFullYear() + '').substr(4 - RegExp.$1.length))
    }
    for (var k in date) {
        if (new RegExp("(" + k + ")").test(format)) {
            format = format.replace(RegExp.$1, RegExp.$1.length == 1 ? date[k] : ("00" + date[k]).substr(("" + date[k]).length))
        }
    }
    return format
}

capitalize = (str) => {
    return str.charAt(0).toUpperCase() + str.slice(1)
}

string2Bin = (str) => {
    var result = []
    for (var i = 0; i < str.length; i++) {
        result.push(str.charCodeAt(i))
    }
    return result
}

bin2String = (array) => {
    return String.fromCharCode.apply(String, array)
}

string2arr = (str) => {
    str = str.replace(/{/g, "[").replace(/}/g, "]")
    return JSON.parse(str)
}

string2format = (str, ...args) => {
    if (str.indexOf("{") < 0) {
        return args.join(str)
    }
    return str.format(...args)
}

randomString = () => {
    return Math.random().toString(36).substr(2)
}

isPhone = (str) => {
    var reg = /^[1][2-9][0-9]{9}$/
    return reg.test(str)
}