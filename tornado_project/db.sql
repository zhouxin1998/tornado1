drop database ihome;
create database ihome default charset=utf8;

use ihome;

create table ih_user_profile(
  up_user_id bigint unsigned not null auto_increment comment "用户ID",
  up_name varchar(32) not null comment "用户名",
  up_mobile char(11) not null comment "手机号",
  up_passwd varchar(64) not null comment "密码",
  up_real_name varchar(32) null comment "真实姓名",
  up_id_card varchar(20) null comment "身份证号",
  up_avatar varchar(128) null comment "头像",
  up_admin bit not null default 0 comment "是否管理员",
  up_utime datetime not null default current_timestamp on update current_timestamp comment "最后更新时间",
  up_ctime datetime not null default current_timestamp comment "创建时间",
  primary key (up_user_id),
  unique (up_name),
  unique (up_mobile)
) engine=InnoDB auto_increment=10000 default charset=utf8 comment="用户信息表";

create table ih_area_info(
  ai_area_id bigint unsigned not null auto_increment comment "区域ID",
  ai_name varchar(32) not null comment "区域名称",
  ai_ctime datetime not null default current_timestamp comment "创建时间",
  primary key (ai_area_id)
) ENGINE=InnoDB default charset=utf8 comment="房源区域表";

create table ih_house_info(
  hi_house_id bigint unsigned not null auto_increment comment "房屋ID",
  hi_user_id bigint unsigned not null comment "用户id",
  hi_title varchar(64) not null comment "房屋名称",
  hi_price int not null default 0 comment "房屋价格 单位分",
  hi_area_id bigint unsigned not null comment "房屋区域id",
  hi_address varchar(256) not null default '' comment "地址",
  hi_room_count tinyint unsigned not null default '1' comment "房间数",
  hi_acreage int not null default 0 comment "房间面积",
  hi_house_unit varchar(32) NOT NULL DEFAULT '' comment "房屋户型",
  hi_capacity int not null default 1 comment "可住人数",
  hi_beds varchar(32) not null default '' comment "床的配置",
  hi_deposit int not null default 0 comment "押金，单位分",
  hi_min_days int not null default 1 comment "最短入住时间",
  hi_max_days int not null default 0 comment "最长入住时间,0-不限",
  hi_order_count int not null default 0 comment "下单数量",
  hi_verify_status tinyint not null default '0' comment "审核状态，０-待审核,2-通过审核",
  hi_online_status tinyint not null default '1' comment "0-下线，1-上线",
  hi_index_image_url varchar(256) null comment "房屋主图片url",
  hi_utime datetime not null default current_timestamp on update current_timestamp comment "最后更新时间",
  hi_ctime datetime not null default current_timestamp comment "创建时间",
  primary key (hi_house_id),
  key hi_status (hi_verify_status, hi_online_status),
  constraint foreign key (hi_user_id) references ih_user_profile (up_user_id),
  constraint foreign key (hi_area_id) references ih_area_info (ai_area_id)
) ENGINE=InnoDB default charset=utf8 comment="房屋信息表";

create table ih_house_facility(
  hf_id bigint unsigned not null auto_increment comment "自增id",
  hf_house_id bigint unsigned not null comment "房屋id",
  hf_facility_id int unsigned not null comment "房屋设施",
  hf_ctime datetime not null default current_timestamp comment "创建时间",
  primary key (hf_id),
  constraint foreign key (hf_house_id) references ih_house_info (hi_house_id)
) ENGINE=InnoDB default charset=utf8 comment="房屋设施表";

create table ih_facility_catelog(
  fc_id bigint not null auto_increment comment "自增id",
  fc_name varchar(32) not null comment "设施名称",
  fc_ctime datetime not null default current_timestamp comment "创建时间",
  primary key (fc_id)
) ENGINE=InnoDB default charset=utf8 comment="设施型录表";


create table ih_order_info(
  oi_order_id bigint unsigned not null auto_increment comment "订单表",
  oi_user_id bigint unsigned not null comment "用户id",
  oi_house_id bigint unsigned not null comment "房屋id",
  oi_begin_date date not null comment "入住时间",
  oi_end_data date not null comment "离开时间",
  oi_days int unsigned not null comment "入住天数",
  oi_house_price int unsigned not null comment "房屋单价，单位分",
  oi_amount int unsigned not null comment "订单金额，单位分",
  oi_satatus tinyint not null default '0' comment "订单状态，0-待接单，1-待支付，2-已支付，3-待评价，4-已完成，5-已取消，6-拒接单",
  oi_comment text null comment "订单评论",
  oi_utime datetime not null default current_timestamp on update current_timestamp comment "最后更新时间",
  oi_ctime datetime not null default current_timestamp comment "创建时间",
  primary key (oi_order_id),
  key oi_satatus (oi_satatus),
  constraint foreign key (oi_user_id) references ih_user_profile (up_user_id),
  constraint foreign key (oi_house_id) references ih_house_info (hi_house_id)
) ENGINE=InnoDB default charset=utf8 comment="订单表";

create table ih_house_image(
  hi_image_id bigint unsigned not null auto_increment comment "图片id",
  hi_house_id bigint unsigned not null comment "房屋id",
  hi_url varchar(256) not null comment "图片url",
  hi_ctime datetime not null default current_timestamp comment "创建时间",
  primary key (hi_image_id),
  constraint foreign key (hi_house_id) references ih_house_info (hi_house_id)
) ENGINE=InnoDB default charset=utf8 comment="房屋图片表";














