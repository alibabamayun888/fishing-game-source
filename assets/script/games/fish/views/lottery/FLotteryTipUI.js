/**
 * 抽奖提示
 */

var UIBase = require("UIBase")

cc.Class({
    extends: UIBase,

    properties: {
        txt_type: {
            default: null,
            type: cc.Label
        },
        txt_num: {
            default: null,
            type: cc.Label
        },
    },

    init(args) {
        args = args || {}
        this._super()

        this._lottery = args.lottery
        this._less = args.less
        this._lessName = args.lessName
        this._callback = args.callback
    },

    onLoad () {
        this._super()

        this.txt_type.string = this._lottery
        this.txt_num.string = this._less + this._lessName
    },

    start () {

    },

    update (dt) {

    },

    onConfirm(sender, data) {
        if (typeof this._callback == "function") {
            this._callback()
        }
        this.onClose()
    },

});
