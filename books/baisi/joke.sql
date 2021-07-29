
drop table if exists joke_xiubai;

CREATE TABLE `joke_xiubai` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT comment '自增id',
  `id_from_src` varchar(15) DEFAULT NULL comment '来源的id',
  `theme_id` varchar(30) DEFAULT NULL comment '主题id',
  `type` varchar(20) DEFAULT NULL comment '类型',
  `text` text DEFAULT NULL comment '文本内容',
  `user_id` varchar(15) DEFAULT NULL comment '用户id',
  `user_name` varchar(30) DEFAULT NULL comment '用户名',
  `user_head` varchar(200) DEFAULT NULL comment '用户头像',
  `src` varchar(30) DEFAULT NULL comment '来源',
  `up` int(11) DEFAULT 0 comment '赞数量',
  `down` int(11) DEFAULT 0 comment '踩数量',
  `comment` int(11) DEFAULT 0 comment '评论数量',
  `forward` int(11) DEFAULT 0 comment '转发数量',
  `passtime` datetime comment '源更新时间',
  `cate` varchar(30) DEFAULT NULL comment '标签',
  `obj_url` varchar(200) DEFAULT NULL comment '目标url',
  `download_url` varchar(200) DEFAULT NULL comment '下载url',
  `thumb_url` varchar(200) DEFAULT NULL comment '预览url',
  `width` int(11) DEFAULT 0 comment '宽',
  `height` int(11) DEFAULT 0 comment '高',
  `duration` int(11) DEFAULT 0 comment '视频长度，单位秒',
  `top_comments` text DEFAULT NULL comment 'top评论',
  `create_time` timestamp DEFAULT CURRENT_TIMESTAMP comment '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

alter table joke_xiubai convert to character set utf8mb4 collate utf8mb4_bin;

create index idx_id_from_src on joke_xiubai
(
   id_from_src
);