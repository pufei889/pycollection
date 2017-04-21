<?php
/*    WordPress 发布接口，可以配合火车头采集器使�?

      本接口是在rq204的接口上完善实现，主要增加以下功能：

      1.  随机时间安排与预约发布功能： 可以设定发布时间以及启用预约发布功能
      2. 服务器时间与博客时间的时区差异处理。这特别适合在国外服务器上的博客
      3. 永久链接的自动翻译设置。根据标题自动翻译为英文并进行seo处理
      4. 增加了对分类catagory的处�?
      5. 多标签处�?多个标签可以用火车头默认的tag|||tag2|||tag3的形�?
      6.增加了发文后ping功能
      7.增加了“pending review”的设置

    使用步骤 �?
    1. 修改下面的发布参数，并将hm-locywp文件夹上传到服务器上Wordpress的根目录�?

 */
$postStatus     = "publish"; 			//"future","publish","pending"  预约发布 立即发布 暂不发布
$randomPostTime = 0;//rand(0,50)*rand(200,3000)*24;     //随机发布时间取�?，单位为�?。比�?2345 * rand(0,17)�?为不对时间进行随机处�?当前为一个月之内的随机发�?
$translateSlug  = false;			//自动翻译中文url为拼�?设置为true时可能出现不可预知错�?
$timeZoneOffset = 8;    				//服务器时区与博客时区差别，如服务器为PST(-8)，博客为CST(+8)，则�?6
$pingAfterPost  = false;  				//建议关闭（对于大量发布的情况，开启ping会影响速度，并可能会影响收录）
$postAuthor     = 1;    				//作者的id，默认为admin
$secretWord     = "yht123hito"; 			//接口验证密码请不要更�?更改后将导致发布失败


//同义词替换功�?(区分大小�?关键词库用word.txt表示)
function strtr_words($str)
{
    $words=array();
    $key_list = file("word.txt");
    foreach($key_list as $k=>$v)
    {
        $str_data = explode(",",$v);//关键词分割符
        $w1=trim($str_data[0])." ";
        $w2=trim($str_data[1])." ";
        $words+=array("$w1"=>"$w2","$w2"=>"$w1");
    }
    return strtr($str,$words);//返回结果
}

function get_remote_img($content,$imgdir){
    $tmp = stripslashes($content);
    preg_match_all("/<img.*src=.*(https?[^\"\'\s]*)/i",$tmp,$match);
    $imgarr=($match[1])?$match[1]:array();
    foreach($imgarr as $img){
        $imgraw = file_get_contents($img);
        usleep(100);
        $subfix = substr($img,strrpos($img,"."));
        if($imgraw){
            $filename = rand().$subfix;
            file_put_contents(dirname(__FILE__)."/..".$imgdir."/".$filename,$imgraw);
            $content = str_replace($img,"$imgdir$filename",$content);
        }
    }
    return $content;
}
function changepostdate($maxaday,$mininterval=6000){
    global $DB,$table_prefix;
    $sql = "select count(id) as num from ".$table_prefix."posts where 1";
    $res = $DB->query($sql);
    $tmp = $DB->fetch_array($res);
    $num = $tmp['num'];
    $days = floor($num/$maxaday);
    $maxinterval = floor(24*3600/$maxaday);
    //���ڵ�ʱ���
    $now = time();
    $offset=0;
    while($days>0){
        //��ȡ��һ�����µ�������Ŀ�ʼʱ��
        $starttime = $now-$days*3600*24;
        $tmp = $DB->query("select id from $table_prefix"."posts where 1 order by id asc limit $offset,$maxaday");
        while($tmp2=$DB->fetch_array($tmp)){
            $id=$tmp2["id"];
            $posttime =$starttime+rand($mininterval,$maxinterval);
            $DB->query("update $table_prefix"."posts set post_date=from_unixtime($posttime),post_date_gmt=from_unixtime($posttime) ,post_modified=from_unixtime($posttime),post_modified_gmt=from_unixtime($posttime) where id=$id");
        }
        $days--;
        $offset = $offset+$maxaday;
    }
}
