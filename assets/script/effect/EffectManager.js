/**
 * 动效管理单例
 */


var EffectManager = cc.Class({
    extends: cc.Component,

    properties: {

    },

    // onLoad () {},

    start() {

    },

    /**
    执行特效
    @param effType  function  特效类型
    @param ...              不定长参数列表
    */
    doEffectAPI(effType, ...args) {
        if (effType) {
            effType(...args)
        }
    },

})

EffectManager.getInstance = function () {
    if (EffectManager.instance == null) {
        EffectManager.instance = new EffectManager()
    }
    return EffectManager.instance
}
