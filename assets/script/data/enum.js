/**
 * 全局枚举
 */

ENUM = {}

ENUM.ITEM_ID = {
    COIN: 10010001,
    DIAMOND: 10010002,
    LOTTERY: 10010003,
    RMB: 10010004,
    SCORE: 10010008,
    RED_DOT: 20040002,
    LOCK: 20030001,
    ICE: 20030002,
    RAGE: 20030003,
    SUMMON: 20030005,
    BUGLE: 20030007,
    LASER: 0,
    ENERGY: 20070003,
    MISSILE1: 20010001,
    MISSILE2: 20010002,
    MISSILE3: 20010003,
    MISSILE4: 20010004,
    ENCHANCE: 20070001,
    HORN: 20060001,
    EXCHANGE_CMD: 20070004,
}

ENUM.ITEM_TYPE = {
    BULLET: 2001,
    BOX: 2002,
    HORN: 2006,
}

ENUM.EXCHANGE_ID = {
    MISSILE: 25,
}

ENUM.ROOM_ID = {
    FREE_MATCH: 101,
    GRAND_PRIX: 102,
}

// 商城道具ID
ENUM.SHOP_ID = {
    ONEYUAN: 101,  // 1元礼包
    GUIDEGIFT: 102,  // 新人豪礼
    GOUP: 103,  // 直升礼包
    HUNT: 104,  // 猎魔礼包
    MONTHCARD: 207,  // 月卡
    NOBILITY: 401,  // 贵族礼包
    FIRSTRECHARGE: 501,  // 首充礼包
}

// 破产补偿
ENUM.REDRESS_ID = 100001
// 炮倍
ENUM.CANNON_SEP_MULTI = 1000
// 狂暴皮肤
ENUM.RAGE_SKIN_ID = 3000001


////////////////////////////////////////
// 前后端协议号
ENUM.CMD = {
    SERVER_INFO: 10000,
    SERVER_LOGIN: 10001,
    HEART_BEAT: 10008,
}

////////////////////////////////////////
// 错误码
ENUM.ERR_CODE = {
    EXCHANGE: 17001,        // 兑换道具不足
    KICK_OUT: 10007002,     // 封号
    LOGIN_OTHER: 10007001,     // 顶号/踢号
    LOGIN_OTHER2: 10006,        // 顶号/踢号
    LIMIT_CANNON: 80006005,     // 经典场炮倍不足
    LIMIT_CANNON2: 80006006,     // 特殊场炮倍不足
    HALL_STATE: 88888,        // 大厅状态变化
}

////////////////////////////////////////
// 场景ID
ENUM.SCENCE = {
    LOGO: 1,
    LOGIN: 2,
    PLATEFORM: 3,
    FISH: 1018,
}

////////////////////////////////////////
// UI层级
ENUM.UI_Z = {
    TOP: 3000,
    TIP: 2000,
    MSG: 1024,
    DIALOG: 400,
    UI: 100,
}

////////////////////////////////////////
// 默认资源
ENUM.DEFAULT = {
    FONT: "gameres/fonts/simhei.ttf",
    SPINE: { res: "gameres/general/spine/upload/dt_jiazai", ani: "1" },
    TOUCH: { res: "gameres/general/spine/guangquan/dt_gq", ani: "1" },
    IMAGE: "gameres/general/board/TouMing.png",
    TIMER: "gameres/general/board/pn_bar_15.png",
    SCREENSHOT: "gameres/general/bg/bg_pic_4.jpg",
    CAPTURE: "screenshot.jpg",
    PLACEHOLDER: "#ffffff",
    SHADER: {
        shadow: "shadow", // 阴影
        // blur    : "blur",   // 模糊
    },
}

// 颜色
COLOR = {
    BLACK: cc.color(0, 0, 0),
    DARK: cc.color(128, 128, 128),
    WHITE: cc.color(255, 255, 255),
    GREEN: cc.color(0, 255, 0),
}

// 动效 
EffType = {
    shader 		: (...args) => { setShader(...args) },	// 着色
	adrift 		: (...args) => { adrift(...args) },		// 漂浮效果
	breathe 	: (...args) => { breathe(...args) },	// 呼吸效果
	bubble 		: (...args) => { bubble(...args) },		// 冒泡效果
	ripple 		: (...args) => { ripple(...args) },		// 波动效果
	rippleOut 	: (...args) => { rippleOut(...args) },	// 波动消失
	floating	: (...args) => { floating(...args) },	// 悬浮
	rock		: (...args) => { rock(...args) },		// 摇晃
	zoom		: (...args) => { zoom(...args) },		// 缩放
	zoomOut		: (...args) => { zoomOut(...args) },	// 缩小
	flyTo		: (...args) => { flyTo(...args) },		// 飞向
	beton		: (...args) => { moveAndBack(...args) },// 押注
	flop		: (...args) => { flop(...args) },		// 翻转
	jelly		: (...args) => { jelly(...args) },		// 果冻Q弹
	blink		: (...args) => { blink(...args) },		// 闪烁
	lapa		: (...args) => { startLapa(...args) },	// 拉霸
	tour		: (...args) => { tour(...args) },		// 鱼巡游
	slideIn		: (...args) => { slideIn(...args) },	// 滑入
	slideOut	: (...args) => { slideOut(...args) },	// 滑出
}

EffDir = {
    top: 1,
    left: 2,
    center: 3,
    right: 4,
    bottom: 5,
}

// 道具过滤列表
ItemFilter = [10010001, 10010002, 20010001, 20010002, 20010003, 20010004, 20030001, 20030002]

// 领奖状态
RewardState = {
    disable : 0,
    enable : 1,
    received : 2,
}

// 商城栏目
ShopType = {
    gold    : 1,
    ticket  : 2,
    prop    : 3,
    diamond : 3,
    fort    : 5,
    all     : 3,
}
// 商品状态
ShopState = {
    default     : 0, // 默认
    hide        : 1, // 隐藏
    verifier    : 2, // 审核中
    sellout     : 3, // 售罄
}

// 兑换栏目
ExchangeType = {
    all     : 0, // 所有
    tel     : 1, // 话费卡
    real    : 2, // 实物
    redpack : 3, // 红包
    bullet  : 4, // 弹头
    prop    : 5, // 道具
}
// 兑换状态
ExchangeStatus = ["处理", "已处理", "已发货", "已完成"]
