/**
 * 辅助类
 */

isEmpty = (obj) => {
    if (obj === undefined) return true
    if (obj === null) return true
    if (obj === "") return true
    if (obj === 0) return true
    if (obj instanceof Array && obj.length == 0) return true
    if (typeof obj == "object" && sizeOf(obj) == 0) return true

    return false
}

md5Str = (str) => {
    return require("MD5").hex_md5(str)
}

rotatePoints = () => {

}

circleHitPolygons = () => {

}

performWithDelay = (node, func, delay, tag) => {
    if (node) {
        var seq = [
            cc.delayTime(delay),
            cc.callFunc(func)
        ]
        var act = cc.sequence(seq)
        if (tag) {
            act.setTag(tag)
        }
        node.runAction(act)
        return act
    }
    return null
}

adapterCoord = (x, y) => {
    // todo
    return cc.v2(x, y)
}

/**
根据等级转换成炮倍
服务端统一传等级 客户端解码
*/
fromLvGetCannonMult = (lv) => {
    if (!lv || !BYCannonLevelConfig[lv]) {
        return 1
    }
    return BYCannonLevelConfig[lv].cannon_multiple
}

/**
从CDN服务器获取图片资源并展示
@param node         cc.Node         控件
@param cdnImg       String          图片资源URL
*/
setCDNImg = (node, cdnImg) => {
    if (!isEmpty(cdnImg)) {
        if (!cdnImg.endWith("jpg") && !cdnImg.endWith("png")) {
            cdnImg = cdnImg + "?aa=aa.jpg"
        }
        cc.loader.load(cdnImg, (err, texture) => {
            var spr = node.getComponent(cc.Sprite)
            var size = node.getContentSize()
            if (spr) {
                var frame = new cc.SpriteFrame(texture)
                spr.spriteFrame = frame
                node.setContentSize(size)
            }
        })
    }
}

/**
物品数量显示格式化
@param id       number  物品ID
@param count    number  物品数量
@param prefix   string  前缀 ["x"]
@return string
*/
formatCount = (id, count, prefix, ignoreMeasure) => {
    prefix = prefix || "x"
    var ret
    if (id === ENUM.ITEM_ID.LOTTERY) {
        ret = measure(count, 2, 2, true)
    } else if (ignoreMeasure) {
        ret = prefix + count
    } else {
        ret = prefix + measure(count)
    }
    return ret
}