/**
 * 列表工具
 */

// 按指定位置删除
Array.prototype.remove = function (index) {
    var ret
    if (index > - 1) {
        ret = this[index]
        this.splice(index, 1)
    }
    return ret
}

// 按元素名称删除
Array.prototype.removeValue = function (val) {
    var index = this.indexOf(val)
    if (index > - 1) {
        this.splice(index, 1)
    }
}

// 添加元素到指定位置
Array.prototype.insert = function (index, val) {
    if (index > - 1) {
        this.splice(index, 0, val)
    }
}

/**
 * 获取对象的大小
 * @param {Object} o 
 */
sizeOf = (o) => {
    var count = 0
    for (const k in o) {
        if (o.hasOwnProperty(k) && o[k]) {
            count++
        }
    }
    return count
}

keys = (o, filter, key) => {
    var ret = []
    for (const k in o) {
        if (o.hasOwnProperty(k) && o[k]) {
            if (isEmpty(filter)) {
                ret.push(k)
            } else {
                var v = k
                if (!isEmpty(key)) {
                    v = o[k][key]
                }
                if (filter.indexOf(v) >= 0 || filter.indexOf(parseInt(v)) >= 0) {
                    ret.push(k)
                }
            }
        }
    }
    return ret
}

keyOf = (o, v) => {
    for (const k in o) {
        if (o.hasOwnProperty(k) && o[k]) {
            if (v == o[k]) {
                return k
            }
        }
    }
    return null
}

newclone = (o) => {
    if (o instanceof Array) {
        return o.slice(0)
    }
    var ret = {}
    for (const k in o) {
        if (o.hasOwnProperty(k) && o[k]) {
            ret[k] = o[k]
        }
    }
    return ret
}

merge = (dest, src) => {
    for (const key in src) {
        if (src.hasOwnProperty(key) && src[key]) {
            dest[key] = src[key]
        }
    }
    return dest
}

/**
 * 二分查找
 * @param {Array} t 数据表(List)
 * @param {Object} v 查找对象
 * @param {String} k v为table时，匹配key
 * @returns 匹配索引
 */
bsearch = (t, v, k) => {
    var l = 0
    var r = t.length - 1
    var m
    if (r > 0) {
        while (l <= r) {
            m = Math.ceil((l + r) / 2)
            if ((k && t[m][k] <= v) || (!k && t[m] == v)) {
                l = m + 1
            } else {
                r = m - 1
            }
        }
    }
    return r
}

/**
 * 乱序
 */
shuffle = (a) => {
    if (typeof a == 'number') {
        var l = [];
        for (let index = 0; index < a; index++) {
            l.push(index + 1);
        }
        return shuffle(l);
    }
    var len = a.length;
    for (var i = 0; i < len - 1; i++) {
        var index = random(0, len - 1);
        if (index != i) {
            var temp = a[index];
            a[index] = a[i];
            a[i] = temp;
        }
    }
    return a;
}