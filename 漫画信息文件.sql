-- 1. 创建数据库
CREATE DATABASE IF NOT EXISTS manjishe CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 2.使用数据库
USE manjishe;

-- 3.用户表
CREATE TABLE IF NOT EXISTS user(
    id INT PRIMARY KEY AUTO_INCREMENT COMMENT '用户编号',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    pwd VARCHAR(100) NOT NULL COMMENT '登录密码',
    phone VARCHAR(11) NOT NULL UNIQUE COMMENT '手机号'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户信息表';

-- 4.漫画主表
DROP TABLE IF EXISTS comic_info;
CREATE TABLE comic_info (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL COMMENT '漫画名称',
    author VARCHAR(100) NOT NULL COMMENT '作者',
    category VARCHAR(50) NOT NULL COMMENT '分类',
    cover VARCHAR(255) COMMENT '封面图片地址',
    status VARCHAR(20) COMMENT '状态：连载中/完结'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 comment='漫集社漫画信息表';

-- 5.评论表
CREATE TABLE IF NOT EXISTS comment (
	id INT PRIMARY KEY AUTO_INCREMENT,
	comic_id INT NOT NULL,
	username VARCHAR(50) DEFAULT '匿名用户',
	score INT NOT NULL,
	content TEXT NOT NULL,
	create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (comic_id) REFERENCES comic_info(id)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

-- 6.收藏表
CREATE TABLE IF NOT EXISTS favorite(
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    comic_id INT,
    fav_time DATETIME,
    UNIQUE(user_id,comic_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7.阅读记录表
CREATE TABLE IF NOT EXISTS history(
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    comic_id INT,
    read_time DATETIME
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 8.书架表
CREATE TABLE IF NOT EXISTS bookshelf(
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    comic_id INT,
    last_chapter VARCHAR(50),
    UNIQUE(user_id,comic_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 9. 插入35条漫画数据
INSERT INTO comic_info (title, author, category, cover, status) VALUES
('海贼王','尾田荣一郎','热血','static/images/one_piece.jpg','连载中'),
('火影忍者','岸本齐史','热血','static/images/Naruto.jpg','完结'),
('龙珠','鸟山明','热血','static/images/Dragon Ball.jpg','完结'),
('咒术回战','芥见下下','热血','static/images/Jujutsu Kaisen.jpg','连载中'),
('进击的巨人','谏山创','热血','static/images/Attack on Titan.jpg','完结'),
('鬼灭之刃','吾峠呼世晴','热血','static/images/Demon Slayer-Kimetsu no Yaiba.jpg','完结'),
('全职猎人','富坚义博','热血','static/images/Hunter x Hunter.jpg','连载中'),
('一拳超人','村田雄介','热血','static/images/One-Punch Man.jpg','连载中'),
('我的英雄学院','堀越耕平','热血','static/images/My Hero Academia.jpg','完结'),
('死神','久保带人','热血','static/images/Bleach.jpg','完结'),

('辉夜大小姐','赤坂明','校园','static/images/Kaguya-sama-Love is War.jpg','连载中'),
('擅长捉弄的高木同学','山本崇一朗','校园','static/images/Teasing Master Takagi-san.jpg','完结'),
('堀与宫村','HERO','校园','static/images/Horimiya.jpg','完结'),
('五等分的新娘','春场葱','校园','static/images/The Quintessential Quintuplets.jpg','完结'),
('青春期猪头少年','鸭志田一','校园','static/images/Rascal Does Not Dream of Bunny Girl Senpai.jpg','完结'),

('妖精的尾巴','真岛浩','奇幻','static/images/Fairy Tail.jpg','完结'),
('东京复仇者','和久井健','奇幻','static/images/Tokyo Revengers.jpg','连载中'),
('约定的梦幻岛','白海','奇幻','static/images/The Promised Neverland.jpg','完结'),
('地缚少年花子君','あいだいろ','奇幻','static/images/Toilet-Bound Hanako-kun.jpg','连载中'),
('葬送的芙莉莲','山田钟人','奇幻','static/images/Frieren-Beyond Journeys End.jpg','连载中'),

('元气少女缘结神','铃木JULIETTA','恋爱','static/images/Kamisama Kiss.jpg','完结'),
('月刊少女野崎君','椿泉','恋爱','static/images/Monthly Girls Nozaki-kun.jpg','连载中'),
('昼行闪耀的流星','森永爱','恋爱','static/images/Daytime Shooting Star.jpg','完结'),
('恋如雨止','眉月润','恋爱','static/images/After the Rain.jpg','完结'),
('俺物语','河原和音','恋爱','static/images/My Love Story!!.jpg','完结'),

('名侦探柯南','青山刚昌','悬疑','static/images/Detective Conan.jpg','连载中'),
('20世纪少年','浦泽直树','悬疑','static/images/20th Century Boys.jpg','完结'),
('死亡笔记','大场鸫','悬疑','static/images/Death Note.jpg','完结'),
('欺诈游戏','甲斐谷忍','悬疑','static/images/Liar Game.jpg','完结'),
('狂赌之渊','河本焰','悬疑','static/images/Kakegurui.jpg','连载中'),

('铳梦','木城幸人','科幻','static/images/Battle Angel Alita.jpg','完结'),
('攻壳机动队','士郎正宗','科幻','static/images/Ghost in the Shell.jpg','完结'),
('阿基拉','大友克洋','科幻','static/images/Akira.jpg','完结'),
('希德尼亚的骑士','贰瓶勉','科幻','static/images/Knights of Sidonia.jpg','完结'),
('苹果核战记','士郎正宗','科幻','static/images/Appleseed.jpg','完结');

-- 给封面图片路径统一拼接根路径前缀 /，保证前端静态资源正常访问
UPDATE comic_info
SET cover = CONCAT('/', cover)
WHERE cover NOT LIKE '/%';

