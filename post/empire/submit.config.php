<?php
/*帝国面登陆发布的相关配置
*/
//设置时区
date_default_timezone_set("Asia/Shanghai");
$username = "admin";  //文章发布的用户名，需要改成系统中存在的账户
$_POST['classid'] = "1";  //设置文章发布的栏目ID

/*下面的配置不是必须的，请根据需要改动*/
$_POST['title'] = $_POST['post_title'];
$_POST['newstext'] = $_POST['post_content'];
$_POST['news'] = 'AddNews';
$_POST['bclassid'] = '2';
$_POST['id'] = '0';
$_POST['newspath'] = '';
$_POST['filepass'] = time();
$_POST['ecmsnfrom'] = "http://".$_SERVER['HTTP_HOST']."/e/admin/admin.php";
$_POST['titlecolor'] = '';  //标题颜色
$_POST['ftitle'] = "";  //副标题
$_POST['checked'] = '1';
$_POST['keyboard'] = "";  //关键词
$_POST['titleurl'] = "";
$_POST['newstime'] = date("Y-m-d H:m:s");
$_POST['smalltext'] = "";  //内容简介
$_POST['writer'] = "";  //作者
$_POST['befrom'] = "";  //信息来源
$_POST['titlefont'] = array();  //标题样式：bis
$_POST['isgood'] = "0";  //推荐
$_POST['firsttitle'] = "0";  //头条
$_POST['newstempid'] = 1;  //模板编号
$_POST['copyimg'] = 1;  //远程保存图片
$_POST['mark'] = 1;  //图片加水印
$_POST['getfirsttitlepic'] = 1;  //取第1张上传图为标题图片
$_POST['getfirsttitlespic'] = 1;  //取第1张上传图为缩略图
$_POST['getfirsttitlespicw'] = '105';  //缩略图宽
$_POST['getfirsttitlespich'] = '118';  //缩略图高
$_POST['copyflash'] = 1;  //远程保存FLASH
$_POST['qz_url'] = '';  //FLASH地址前缀
$_POST['dokey'] = 1;  //关键字替换
$_POST['autopage'] = 1;  //自动分页
$_POST['autosize'] = 5000;  //自动分页大小，通常设为5000字
$_POST['istop'] = 0;  //置顶级别，0-6级
$_POST['groupid'] = 0;  //访问权限,0为游客，1为普通会员，2为VIP会员，3为企业会员，4为企业VIP会员
$_POST['userfen'] = 0;  //查看扣除点数
$_POST['closepl'] = 1;  //关闭评论
$_POST['filenameqz'] = '';  //文件前缀
$_POST['ztid'] = array();  //所属专题ID
$_POST['onclick'] = 200;  //最大点击数，点击数将取1到最大点击数的随机值；

//结果检测
function check_publish_status($html){
    if(mb_strpos($html,"增加信息成功") === false){
        return "Publish failed!";
    }
        return "Publish success!";
}
