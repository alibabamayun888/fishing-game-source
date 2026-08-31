/**
 * 事件管理
 */

function _getTargetKey(target) {
    return target.uuid.toString().toUpperCase()
}

var EventManager = cc.Class({
    extends: cc.Component,

    ctor() {
        EventManager.instance = this
    },

    properties: {
        _event: [],
    },

    statics: {
        instance: null
    },

    // onLoad () {},

    start() {

    },

    // update (dt) {},

    /**
     * 添加监听
     * @param {String} eventName 事件名
     * @param {cc.Class} target 监听者
     * @param {Function} listener 回调函数
     */
    addEventListener(eventName, target, listener) {
        if (isEmpty(target) || isEmpty(listener)) {
            return
        }
        eventName = eventName.toUpperCase()
        if (!this._event[eventName]) {
            this._event[eventName] = []
        }
        var key = _getTargetKey(target)
        if (!this._event[eventName][key]) {
            this._event[eventName][key] = { target: target, listener: [listener] }
        } else {
            this._event[eventName][key].listener.push(listener)
        }
    },

    /**
     * 派发事件
     * @param {String} eventName 事件名
     * @param {Object} eventData 派发数据
     */
    dispatchEvent(eventName, eventData) {
        if (isEmpty(eventName)) return
        eventName = eventName.toUpperCase()
        if (this._event[eventName]) {
            for (const key in this._event[eventName]) {
                if (this._event[eventName].hasOwnProperty(key) && this._event[eventName][key]) {
                    const v = this._event[eventName][key]
                    if (v.target) {
                        for (let i = 0; i < v.listener.length; i++) {
                            v.listener[i]({ name: eventName, data: eventData })
                        }
                    }
                }
            }
        }
    },

    /**
     * 事件管理
     */
    hasEvent(eventName) {
        eventName = eventName.toUpperCase()
        return this._event[eventName]
    },

    removeEvent(eventName, target) {
        eventName = eventName.toUpperCase()
        if (isEmpty(target)) {
            delete this._event[eventName]
        } else if (this._event[eventName]) {
            var key = _getTargetKey(target)
            delete this._event[eventName][key]
        }
    },

    removeEventByName(eventName) {
        eventName = eventName.toUpperCase()
        delete this._event[eventName]
    },

    removeEventByTarget(target) {
        if (!isEmpty(target)) {
            var key = _getTargetKey(target)
            for (const k in this._event) {
                if (this._event.hasOwnProperty(k) && this._event[k][key]) {
                    delete this._event[k][key]
                }
            }
        }
    },

    removeAllEvent() {
        this._event = []
    }

})

EventManager.getInstance = function () {
    if (EventManager.instance == null) {
        EventManager.instance = new EventManager()
    }
    return EventManager.instance
}
