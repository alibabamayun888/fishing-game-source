/**
 * 捕鱼相关全局定义
 */

// 房间类型
FishRoomType = {
    COIN        : 1,    // 经典场
    HUNT        : 2,    // 猎魔场
    MATCH       : 3,    // 比赛场
}
FishRoomID = {
    captain     : 4,    // 幽灵船长
}
// 技能
FSkill = {
    lock        : 1001, // 锁定
    ice         : 1002, // 冰封
    rage        : 1003, // 狂暴
    summon      : 1004, // 召唤
    laser       : 1005, // 激光
    bugle       : 1006, // 号角
    nbomb       : 1009, // 核弹
}
// 弹头列表
FMissile = [
    {cannon : 2000000001, item : 20010001},
    {cannon : 2000000002, item : 20010002},
    {cannon : 2000000003, item : 20010003},
    {cannon : 2000000004, item : 20010004},
]
// 开火返回结果
FireResult = {
    SUCCESS     : 0,    // 成功
    CANNON      : -1,   // 炮倍不足
    FRENZY      : -2,   // 狂暴金币不足
    COIN        : -3,   // 金币不足
    BULLET      : -4,   // 子弹过多
}
// 炮台列表
CannonType = {
    normal      : 1,    // 普通
    vip         : 2,    // 会员
    rage        : 3,    // 狂暴
    laser       : 4,    //激光
}
// 背景数量
BG_MAX = 3
BGM_MAX = 2

// 鱼的状态
FishState = {
    swim        : "run",
    hit         : "hit",
    escape      : "escape",
    die         : "die",
    idle        : "idle",
    lightning   : "lightning",
}
FishStateIdx = [
    "die",
    "hit",
    "lightning",
    "run",
    "escape",
    "idle",
]

// 鱼击杀状态
FishHitState = {
    die         : 0,    // 被击杀
    hurt        : 1,    // 受伤未死亡
    funerary    : 2,    // 陪葬（被炸弹或者雷电之类的）
}
// 鱼类型
FishType = {
    normal      : 1,    // 普通鱼
    net         : 2,    // 一网打尽
    lighting    : 3,    // 雷龙
    bomb        : 4,    // 半屏炸弹
    king        : 5,    // 鱼王
    boss        : 6,    // BOSS
    bonus       : 7,    // 奖金鱼
    bullet      : 8,    // 弹头场专属
    hunt        : 9,    // 猎魔场专属
}
// 奖金盘类型
PlateType = {
    none        : 0,
    normal      : 1,
    full        : 2,
}

// 碰撞检测类型
CollideType = {
    polygon     : 1,
    rect        : 2,
    circle      : 3,
}