-- 1. 创建数据库
CREATE DATABASE IF NOT EXISTS manjishe CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2. 使用数据库
USE manjishe;

-- 3. 创建漫画表
DROP TABLE IF EXISTS comic_info;
CREATE TABLE comic_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL COMMENT '漫画名称',
    author VARCHAR(100) NOT NULL COMMENT '作者',
    category VARCHAR(50) NOT NULL COMMENT '分类',
    cover VARCHAR(255) COMMENT '封面图片地址',
    status VARCHAR(20) COMMENT '状态：连载中/完结'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='漫集社漫画信息表';

-- 4. 插入50条漫画数据
INSERT INTO comic_info (title, author, category, cover, status) VALUES
('海贼王','尾田荣一郎','热血','https://picsum.photos/300/400','连载中'),
('火影忍者','岸本齐史','热血','https://picsum.photos/300/400','完结'),
('龙珠','鸟山明','热血','https://picsum.photos/300/400','完结'),
('咒术回战','芥见下下','热血','https://picsum.photos/300/400','连载中'),
('进击的巨人','谏山创','热血','https://picsum.photos/300/400','完结'),
('鬼灭之刃','吾峠呼世晴','热血','https://picsum.photos/300/400','完结'),
('全职猎人','富坚义博','热血','https://picsum.photos/300/400','连载中'),
('一拳超人','村田雄介','热血','https://picsum.photos/300/400','连载中'),
('我的英雄学院','堀越耕平','热血','https://picsum.photos/300/400','完结'),
('死神','久保带人','热血','https://picsum.photos/300/400','完结'),

('辉夜大小姐','赤坂明','校园','https://picsum.photos/300/400','完结'),
('擅长捉弄的高木同学','山本崇一朗','校园','https://picsum.photos/300/400','完结'),
('堀与宫村','HERO','校园','https://picsum.photos/300/400','完结'),
('五等分的新娘','春场葱','校园','https://picsum.photos/300/400','完结'),
('青春期猪头少年','鸭志田一','校园','https://picsum.photos/300/400','完结'),

('妖精的尾巴','真岛浩','奇幻','https://picsum.photos/300/400','完结'),
('东京复仇者','和久井健','奇幻','https://picsum.photos/300/400','连载中'),
('约定的梦幻岛','白海石','奇幻','https://picsum.photos/300/400','完结'),
('地缚少年花子君','あいだいろ','奇幻','https://picsum.photos/300/400','连载中'),
('葬送的芙莉莲','山田钟人','奇幻','https://picsum.photos/300/400','连载中'),

('元气少女缘结神','铃木JULIETTA','恋爱','https://picsum.photos/300/400','完结'),
('月刊少女野崎君','椿泉','恋爱','https://picsum.photos/300/400','完结'),
('昼行闪耀的流星','森永爱','恋爱','https://picsum.photos/300/400','完结'),
('恋如雨止','眉月润','恋爱','https://picsum.photos/300/400','完结'),
('俺物语','河原和音','恋爱','https://picsum.photos/300/400','完结'),

('名侦探柯南','青山刚昌','悬疑','https://picsum.photos/300/400','连载中'),
('伊藤润二精选集','伊藤润二','悬疑','https://picsum.photos/300/400','完结'),
('死亡笔记','大场鸫','悬疑','https://picsum.photos/300/400','完结'),
('欺诈游戏','甲斐谷忍','悬疑','https://picsum.photos/300/400','完结'),
('狂赌之渊','河本焰','悬疑','https://picsum.photos/300/400','连载中'),

('钢之炼金术师','荒川弘','科幻','https://picsum.photos/300/400','完结'),
('赛博朋克','山本佳奈','科幻','https://picsum.photos/300/400','连载中'),
('来自深渊','土笔章人','科幻','https://picsum.photos/300/400','连载中'),
('命运石之门','5pb.','科幻','https://picsum.photos/300/400','完结'),
('阿凡达漫画','卡梅隆','科幻','https://picsum.photos/300/400','完结'),

('夏目友人帐','绿川幸','治愈','https://picsum.photos/300/400','完结'),
('龙猫官方漫画','宫崎骏','治愈','https://picsum.photos/300/400','完结'),
('蜂蜜与四叶草','羽海野千花','治愈','https://picsum.photos/300/400','完结'),
('擅长逃跑的殿下','松浦健人','治愈','https://picsum.photos/300/400','连载中'),
('玉子爱情故事','京阿尼','治愈','https://picsum.photos/300/400','完结'),

('狐妖小红娘','小新','古风','https://picsum.photos/300/400','连载中'),
('一人之下','米二','古风','https://picsum.photos/300/400','连载中'),
('刺客伍六七','何小疯','古风','https://picsum.photos/300/400','完结'),
('天行九歌','玄机科技','古风','https://picsum.photos/300/400','连载中'),
('少年锦衣卫','柏言映画','古风','https://picsum.photos/300/400','完结'),

('排球少年','古馆春一','竞技','https://picsum.photos/300/400','完结'),
('黑子的篮球','藤卷忠俊','竞技','https://picsum.photos/300/400','完结'),
('头文字D','重野秀一','竞技','https://picsum.photos/300/400','完结'),
('棒球英豪','安达充','竞技','https://picsum.photos/300/400','完结'),
('飙速宅男','渡边航','竞技','https://picsum.photos/300/400','连载中');cmanjishecomic_infoomic_info