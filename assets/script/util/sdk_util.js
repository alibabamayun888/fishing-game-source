/**
 * 平台辅助
 */

var marketId = ""
var modelName = ""

getMarketId = () => {
    if (isEmpty(marketId)) {
        marketId = MARKET
        if (cc.sys.os == cc.sys.OS_ANDROID || cc.sys.os == cc.sys.OS_IOS) {
            marketId = marketId + "_" + cc.sys.os
        }
    }
    return marketId
}

getAppVersion = () => {
    return "1.1.0"
}

/**
 * 判断是否有刘海
 */
hasBang = () => {
    if (modelName !== "") {
        return modelName.indexOf("iPhone X") >= 0
    }
    var sysInfo = {}
    if (QQ_GAME) {
        sysInfo = qq.getSystemInfoSync()
    } else if (cc.sys.platform == cc.sys.WECHAT_GAME) {
        sysInfo = wx.getSystemInfoSync()
    } else if (cc.sys.platform == cc.sys.QQ_PLAY) {
        sysInfo = BK.getSystemInfoSync()
    }
    modelName = sysInfo.model || "xxx"
    return modelName.indexOf("iPhone X") >= 0
}

/**
 * 平台是否可以分享
 */
isSharePlatform = () => {
    return QQ_GAME || cc.sys.platform == cc.sys.WECHAT_GAME || cc.sys.platform == cc.sys.QQ_PLAY
}