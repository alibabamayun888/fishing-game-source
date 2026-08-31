/**
 * 事件
 */

const G_Event = {
    NET_PACKET_TIME_OUT: "NET_PACKET_TIME_OUT",
    NET_RECV_PACKET: "NET_RECV_PACKET",
    NET_READY_RECONNECT: "NET_READY_RECONNECT",
    NET_HB_CHECK: "NET_HB_CHECK",
    LOGIN_ERR_EVENT: "LOGIN_ERR_EVENT",
    GAME_ON_LOGOUT_EVENT: "GAME_ON_LOGOUT_EVENT",
    GAME_MONEY_MODIFY_EVENT: "GAME_MONEY_MODIFY_EVENT",
    GAME_SEX_MODIFY_EVENT: "GAME_SEX_MODIFY_EVENT",
    GAME_NICK_MODIFY_EVENT: "GAME_NICK_MODIFY_EVENT",
    GAME_LV_MODIFY_EVENT: "GAME_LV_MODIFY_EVENT",
    GAME_PERSON_MODIFY_IMG: "GAME_PERSON_MODIFY_IMG",
    GAME_RED_POINT_EVENT: "GAME_RED_POINT_EVENT",
    GAME_PERSON_MODIFY_FIRTRECHARGE: "GAME_PERSON_MODIFY_FIRTRECHARGE",
    GAME_PERSON_MODIFY_GUIDEGIFT: "GAME_PERSON_MODIFY_GUIDEGIFT",
    GAME_PERSON_MODIFY_TMGIFT: "GAME_PERSON_MODIFY_TMGIFT",
    GAME_PERSON_MODIFY_VIP: "GAME_PERSON_MODIFY_VIP",
    CHANGE_SCENE_EVENT: "CHANGE_SCENE_EVENT",
    SYSTEM_LIMIT_ERROR: "SYSTEM_LIMIT_ERROR",
    ON_BAG_DATA_UPDATE: "ON_BAG_DATA_UPDATE",
    ON_XCOIN_CHANGE: "ON_XCOIN_CHANGE",
    ON_DIAMOND_CHANGE: "ON_DIAMOND_CHANGE",
    ON_LOTTERY_CHANGE: "ON_LOTTERY_CHANGE",
    ON_VIP_CHANGE: "ON_VIP_CHANGE",
    ON_VIP_EXP_CHANGE: "ON_VIP_EXP_CHANGE",
    CHAT_MARQUEE: "CHAT_MARQUEE",
    CHAT_NORMAL: "CHAT_NORMAL",
    ACTIVITY_UPDATE: "ACTIVITY_UPDATE",
    FISH_UPDATE: "FISH_UPDATE",
    MOREGAME_STATE_CHANGE: "MOREGAME_STATE_CHANGE",
    ON_DIY_HEAD_PICK: "ON_DIY_HEAD_PICK",
    ON_DIY_HEAD_UPLOAD: "ON_DIY_HEAD_UPLOAD",
    ON_MYSTERAL_UPDATE: "ON_MYSTERAL_UPDATE",
    UI_ORIENTION_CHANGE: "UI_ORIENTION_CHANGE",
    GAME_LOST_PROTECTION: "GAME_LOST_PROTECTION",
    TASK_CHANGE: "TASK_CHANGE",
    TASK_DONE: "TASK_DONE",
    TASK_FINISH: "TASK_FINISH",
    ON_REDRESS_CHANGE: "ON_REDRESS_CHANGE",
    ON_RECHARGE_FINISH: "ON_RECHARGE_FINISH",
    CLEAN_RED_POINT: "CLEAN_RED_POINT",
    ENTER_WEEK_HAPPY: "ENTER_WEEK_HAPPY",
    ACCELERATION_CHANGE: "ACCELERATION_CHANGE",
}

/**
 * 添加全局事件
 * @param {String} func 功能模块
 * @param {String} key 关键字
 * @param {String} value 事件名称
 * @see
 *      addGlobalEvent("bag", "update", "event_bag_update")
 *      addGlobalEvent("bag", "update")
 *      addGlobalEvent("bag_update")
 */
addGlobalEvent = (func, key, value) => {
    var k = func
    if (key) {
        k = k + "_" + key
    }
    value || (value = k)
    G_Event[k.toUpperCase()] = value.toUpperCase()
}

setGlobalEvent = (func, key, value) => {
    addGlobalEvent(func, key, value)
}

/**
 * 获取全局事件
 * @param {String} func 功能模块
 * @param {String} key 关键字
 */
getGlobalEvent = (func, key) => {
    var k = func
    if (key) {
        k = k + "_" + key
    }
    return G_Event[k.toUpperCase()]
}

GEvent = (func, key) => {
    return getGlobalEvent(func, key)
}

