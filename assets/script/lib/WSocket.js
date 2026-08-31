/**
 * WebSocket通讯
 */

window.onfire || (window.onfire = require("onfire"))

var WSocket = {
    _sock: {},

    _onOpen() {
        onfire.fire("onopen")
    },

    _onClose(err) {
        onfire.fire("onclose", err)
    },

    _onMessage(obj) {
        onfire.fire("onmessage", obj)
    },

    isConnenct() {
        return this._sock && this._sock.readyState == 1
    },

    connect(domain) {
        if (this._sock.readyState !== 1) {
            this._sock = new WebSocket(domain)
            this._sock.binaryType = "arraybuffer"
            this._sock.onopen = this._onOpen.bind(this)
            this._sock.onclose = this._onClose.bind(this)
            this._sock.onmessage = this._onMessage.bind(this)
        }
    },

    send(buff) {
        this._sock.send(buff)
    },

    close() {
        this._sock.close()
    }
}

module.exports = WSocket