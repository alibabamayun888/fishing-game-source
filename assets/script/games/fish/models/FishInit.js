// 背包入口文件

var FishInit = {
    _checkLimit(field) {
        if (!field) {
            return [false, false]
        }

        var myCoin = Game.doPluginAPI("get", "playerCoin")
        var v = BYRoomConfig[field+1].coin_area_k
        v = v.coin || v
        if (v[0] <= myCoin && (v[1] >= myCoin || v[1] == 0)) {
            return [false, false]
        }

        Game.doPluginAPI("check", "gold", v[0], true)

        return [true, v[0] > myCoin]
    },

    _enterField(field, params) {
        var limitInfo = this._checkLimit(field)
        var limit = limitInfo[0]
        var isLess = limitInfo[1]
        if (limit) {
            if (!isLess) {
                Game.tipMsg("金币不足")
            }
        } else {
            if (!field) {
                Game.fieldId = field
            } else {
                Game.fieldId = field + 1
            }

            stopAllSounds()
            Game.fishCom.onEnter(true, () => {
                Game.tipMsg("当前炮倍不符合进入门槛！")
            })
        }
    },

    init() {
        var FishUtilTest = false
        var self = this

        // 创建类全局DB和Com对象
        Game.fishDB = new (require("FishDB"))()
        Game.fishCom = new (require("FishCom"))()
        Game.fishMng = new (require("FishMng"))()

        // 注册入口函数
        Game.registerAPI("enter", "fish", (field) => {
            self._enterField(field)
        })
        Game.registerAPI("enter", "field1", () => {
            self._enterField(1)
        })
        Game.registerAPI("enter", "field2", () => {
            self._enterField(2)
        })
        Game.registerAPI("enter", "field3", () => {
            self._enterField(3)
        })

        // 注册相关API,方便其他模块调用
        var apiList = [
            ["enter", "field", (...args) => {
                return self._enterField(...args)
            }],
            ["exit", "fish", (...args) => {
                return Game.fishCom.onExitGame(...args)
            }],
        ]
        Game.registerAPIList(apiList)

        // 注册协议收包对应的解析表key
        Game.registerParsePack(slg_cmd.fish)

        // 注册协议收包对应的解析函数
        var pushCallbackList = [
            [slg_cmd.fish.skill[0], (...args) => {
                Game.fishCom.replyUseSkill(...args)
            }],
            [slg_cmd.fish.updPlayer[0], (...args) => {
                Game.fishCom.replyPlayerUpdate(...args)
            }],
            [slg_cmd.fish.bbsLeave[0], (...args) => {
                Game.fishCom.replyPlayerEnterOrExit(...args)
            }],
            [slg_cmd.fish.bbsShort[0], (...args) => {
                Game.fishCom.replyShoot(...args)
            }],
            [slg_cmd.fish.bbsUpdCannon[0], (...args) => {
                Game.fishCom.replyCannonUpdate(...args)
            }],
            [slg_cmd.fish.bbsHit[0], (...args) => {
                Game.fishCom.replyHit(...args)
            }],
            [slg_cmd.fish.bbsUpdRoom[0], (...args) => {
                Game.fishCom.replyRoomUpdate(...args)
            }],
            [slg_cmd.fish.bbsFish[0], (...args) => {
                Game.fishCom.replyAddFish(...args)
            }],
            [slg_cmd.fish.bbsTide[0], (...args) => {
                Game.fishCom.replyTide(...args)
            }],
            [slg_cmd.fish.debug[0], (...args) => {
                Game.fishCom.replyDebugData(...args)
            }],
            [slg_cmd.fish.cannonLv[0], (...args) => {
                Game.fishCom.replyCannonLvUpdate(...args)
            }],
            [slg_cmd.fish.drawInfo[0], (...args) => {
                Game.fishCom.replyLotteryUpdate(...args)
            }],
            [slg_cmd.fish.draw[0], (...args) => {
                Game.fishCom.replyLotteryNotify(...args)
            }],
            [slg_cmd.fish.taskStart[0], (...args) => {
                Game.fishCom.replyTaskStart(...args)
            }],
            [slg_cmd.fish.taskUpdate[0], (...args) => {
                Game.fishCom.replyTaskUpdate(...args)
            }],
            [slg_cmd.fish.taskFinish[0], (...args) => {
                Game.fishCom.replyTaskFinish(...args)
            }],
            [slg_cmd.fish.bugleStart[0], (...args) => {
                Game.fishCom.replyBugleStart(...args)
            }],
            [slg_cmd.fish.bugleFinish[0], (...args) => {
                Game.fishCom.replyBugleFinish(...args)
            }],
            [slg_cmd.fish.changeSkin[0], (...args) => {
                Game.fishCom.replyChangeSki(...args)
            }],
            [slg_cmd.fish.suitExchange[0], (...args) => {
                Game.fishCom.replySuitExchange(...args)
            }],
            [slg_cmd.fish.itemUpdate[0], (...args) => {
                Game.fishCom.replyItemUpdate(...args)
            }],
        ]
        Game.registerPushMsg(pushCallbackList)

        // 注册进入大厅前需要执行的函数(获取相关数据)
        var prepareList = [
            // () => {
            //     Game.fishCom.queryFishData(0, () => {
            //         Game.prepareNext()
            //     })
            // }
        ]
        Game.registerPrepareList(prepareList)
    }
}

module.exports = FishInit