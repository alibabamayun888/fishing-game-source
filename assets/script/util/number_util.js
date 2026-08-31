/**
 * 数学工具类
 */

const PI_DIV_180 = Math.PI / 180
const MeasureUnit = ["十", "元", "千", "万", "十万", "百万", "千万", "亿", "十亿", "百亿", "千亿"]

random = (min, max) => {
    return Math.floor(Math.random() * (max - min + 1)) + min
}

randomFloat = (min, max, precision) => {
    precision || (precision = 1)
    var d = Math.pow(10, precision)
    var r = random(min * d, max * d)
    return r / d
}

clamp = (n, min, max) => {
    return Math.max(min, Math.min(n, max))
}

isInt = (n) => {
    if (typeof n === "number") {
        return Math.floor(n) == Math.ceil(n)
    }
    return false
}

checknumber = (n) => {
    if (typeof n === "number") {
        return n
    }
    if (typeof n === "string") {
        return parseFloat(n) || 0
    }
    return 0
}

/**
 * 角度转弧度
 * @param {number} angle 角度
 */
angle2radian = (angle) => {
    return angle * PI_DIV_180
}

/**
 * 弧度转角度
 * @param {弧度} radian 
 */
radian2angle = (radian) => {
    return radian / PI_DIV_180
}

/**
 * 角度转换
 * @param {number} angle 角度
 */
transformAngle = (angle) => {
    return (angle + 90) % 360
}

/**
 * 判断数值是否在指定范围内
 * @param {number} n 检测数值
 * @param {number} min 下限
 * @param {number} max 上限
 * @param {boolean} ignoreEqual 忽略等于
 */
inRange = (n, min, max, ignoreEqual) => {
    if (ignoreEqual) {
        return n > min && n < max
    }
    return n >= min && n <= max
}

/**
 * 判断数值是否在指定范围外
 * @param {number} n 检测数值
 * @param {number} min 下限
 * @param {number} max 上限
 * @param {boolean} ignoreEqual 忽略等于
 */
outRange = (n, min, max, ignoreEqual) => {
    if (ignoreEqual) {
        return n < min || n > max
    }
    return n <= min || n >= max
}

/**
 * 两点之间的距离
 * @param {number}} x1 
 * @param {number} y1 
 * @param {number} x2 
 * @param {number} y2 
 */
distance = (x1, y1, x2, y2) => {
    return Math.sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1))
}

/**
保留小数位
@param n            number  数值
@param precision    number  精度(保留位数) [0]
@return number
*/
toFixed = (n, precision) => {
    precision = precision || 1
    var d = Math.pow(10, precision)
    var ret = Math.floor(n * d) / d
    return ret
}

/**
数字修改计量单位
@param n            number      数值
@param m            number      计量位数
@param precision    number      保留精度
@param force        boolean     强制计量
@return string
*/
measure = (n, m, precision, force) => {
    if (!parseInt(n)) {
        return n
    }

    n = parseInt(n)
    precision = precision || 2
    if (isEmpty(m)) {
        if (n > 100000000) {
            m = 8 // 亿
        } else {
            m = 4 // 万
        }
    }

    var d = Math.pow(10, m)
    if (n >= d || force) {
        var ret = toFixed(n / d, precision).toString()
        if (ret.indexOf(".") >= 0) {
            ret = ret.replace(/0+$/, "").replace(/\.$/, "")
        }
        return ret + (MeasureUnit[m-1] || "")
    } else {
        return n
    }
}
