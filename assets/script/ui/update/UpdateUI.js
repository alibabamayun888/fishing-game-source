/**
 * 启动场景
 */

// 提示最大数量[1~7]
const TipMax = 2
// 提示间隔
const TipInv = 1

const httpCom = require("HttpCom").getInstance()

var UIBase = require("UIBase")

cc.Class({
    extends: UIBase,

    properties: {
        txtTip: {
            default: null,
            type: cc.Label,
        },
        prgLoading: {
            default: null,
            type: cc.ProgressBar
        },

        _progress: 0,
        _fakeProgress: 5,
        _tick: 0,
    },

    onLoad() {
        this._super()
        this.prgLoading.progress = 0
        this.txtTip.string = ""
    },

    start() {
        var self = this
        this.updateTip()
        this.schedule(() => {
            self.updateTip()
        }, TipInv)

        Game.preStart()
    },

    update(dt) {
        this.updateProgress()

        if (!this._checked) {
            this._tick = this._tick + dt
            if (this._tick > 0.5) {
                this._checked = true
                this.onCheck()
            }
        }
    },

    setProgress(value) {
        this._progress = value
    },

    updateProgress() {
        if (this._fakeProgress < 95) {
            this._fakeProgress += 1
        }
        var progress = Math.max(this._fakeProgress, this._progress)
        this.prgLoading.progress = progress / 100

        if (!this._isLoad && progress >= 100 && Game.preloadState > 1) {
            this._isLoad = true
            var self = this
            this.scheduleOnce(() => {
                Game.gameStart()
                self.onClose()
            }, 0.3)
        }
    },

    updateTip() {
        var tipIdx = random(1, TipMax)
        this.txtTip.string = LoadingTipsConfig[tipIdx].text
    },

    /**
     * 更新检测
     */
    onCheck() {
        var self = this
        var url = PHP_HOST + "cmdcheck.php?udid=wechat&opid=" + getMarketId()
        var cbSucc = function (resv) {
            var t = JSON.parse(resv)
            if (typeof t == "object" && t.plugins) {
                FuncListServer = t.plugins
                // HallServer = {
                //     left: { area: "left", funcs: string2arr(t.hall_left) },
                //     center: { area: "center", funcs: string2arr(t.hall_center) },
                //     right: { area: "right", funcs: string2arr(t.hall_right) },
                //     top: { area: "top", funcs: string2arr(t.hall_top) },
                //     bottom: { area: "bottom", funcs: string2arr(t.hall_bottom) },
                // }

                resetFuncList()
            }

            self.onCheckFinish()
        }
        var cbFail = function (msg) {
            cc.log(msg)
            self.onCheckFinish()
        }
        httpCom.httpGet(url, cbSucc, cbFail)

        this.scheduleOnce(this.onCheckFinish, 5)
    },

    onCheckFinish() {
        this.unscheduleAllCallbacks()
        this._progress = 100
    },
})
