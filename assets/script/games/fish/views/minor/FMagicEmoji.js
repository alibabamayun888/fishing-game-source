/**
 * 魔法表情
 */

cc.Class({
    extends: cc.Component,

    properties: {

    },

    onLoad() {

    },

    start() {

    },

    update(dt) {

    },

    setData(parent, data, run) {
        this._parent = parent || Game.getScene()
        this._posFrom = data.from
        this._posTo = data.to
        this._magicId = data.mid

        this._cfg = MagicEmojiConfig[this._magicId]

        if (run) {
            this.moveAndRun()
        }
    },

    //////////////////////////////////////////-
    // 监听
    spineCompleteLsn(trackEntry, event) {
        var ani = trackEntry.animation.name
        if (this._spine && this._aniLsn && ani == this._aniLsn) {
            var self = this
            Game.performDelay(() => {
                self._spine.removeFromParent()
                self._spine = null
            }, 0.3)
        }
    },

    moveAndRun() {
        var self = this
        var args = {
            res: this._cfg.spine,
            ani: this._cfg.ani_fly || "1",
            aniRun: this._cfg.ani_run || "2",
            duration: this._cfg.duration || 0.7,
        }
        this._aniLsn = args.aniRun
        this._spine = addSpine(args.res, args)
        this._spine.position = this._posFrom
        this._spine.scale = 0.1
        this._spine.getComponent(sp.Skeleton).setCompleteListener((trackEntry, event) => { 
            self.spineCompleteLsn(trackEntry, event) 
        })

        var self = this
        var seq = [
            cc.scaleTo(0.1, 1.0),
            cc.moveTo(args.duration, this._posTo).easing(cc.easeExponentialIn()),
            cc.delayTime(0.1),
            cc.callFunc(() => {
                spChangeAnimation(self._spine.getComponent(sp.Skeleton), args.aniRun, false)
            }),
        ]
        this._spine.runAction(cc.sequence(seq))

        this._parent.addChild(this._spine)
    },

    _noMoveAndRun(pos, angle) {
        var self = this
        var args = {
            res: this._cfg.spine,
            ani: this._cfg.ani_fly || "1",
            isLoop: false,
        }
        this._aniLsn = args.ani
        this._spine = addSpine(args.res, args)
        this._spine.position = pos || this._posTo
        this._spine.getComponent(sp.Skeleton).setCompleteListener((trackEntry, event) => { self.spineCompleteLsn(trackEntry, event) })
        // if (angle ) {
        //     this._spine.setActorRotation(angle)
        // }

        this._parent.addChild(this._spine)
    },

    runTomato() {
        this.moveAndRun()
    },

    runGun() {
        // var radian = cc.pToAngleSelf(cc.pSub(this._posTo, this._posFrom))
        // var angle = 360 - ((720 + radian * 180 / math.pi) % 360)

        // this._noMoveAndRun(this._posFrom, angle)

        // var args = {
        //     res = this._cfg.spine,
        //     ani = this._cfg.ani_run || "2",
        //     isLoop = true,
        // }
        // for i = 1, 4 do
        //     var spine = Actor.new(args.res, args)
        //     spine.active = false
        //     spine.setPosition(this._posFrom)
        //     var delay = i * 0.1
        //     var seq = {
        //         cc.delayTime(delay),
        //         cc.callFunc(function()
        //             spine.active = true
        //         end),
        //         cc.moveTo(0.3, this._posTo),
        //         cc.RemoveSelf.create(),
        //     }
        //     spine.runAction(cc.sequence(seq))
        //     spine.setActorRotation(angle)
        //     this._parent.addChild(spine)
        // }

        // this._parent.performWithDelay(function()
        //     var args = {
        //         res = this._cfg.spine,
        //         ani = this._cfg.ani_target || "3",
        //         isLoop = false,
        //         release = true
        //     }
        //     var spine = Actor.new(args.res, args)
        //     spine.setPosition(this._posTo)
        //     this._parent.addChild(spine)
        // end, 0.4)
    },

    runFlower() {
        this.moveAndRun()
    },

    runWater() {
        this.moveAndRun()
    },

    runBomb() {
        this.moveAndRun()
    },

});
