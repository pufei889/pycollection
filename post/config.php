<?php
/*
 * wordpress发布模块
 */
$postStatus     = "publish"; 			//"future","publish","pending"
$randomPostTime = 0;                    //rand(0,50)*rand(200,3000)*24; 
$translateSlug  = false;			    //
$timeZoneOffset = 0;    				//
$pingAfterPost  = false;  				//
$postAuthor     = 1;    				//
$secretWord     = "yht123hito"; 		//

function get_remote_img($content,$imgdir){
    $tmp = stripslashes($content);
    preg_match_all("/<img.*src=.*(https?[^\"\'\s]*)/i",$tmp,$match);
    $imgarr=($match[1])?$match[1]:array();
    foreach($imgarr as $img){
        $imgraw = pycurl($img);
        usleep(500);
        $subfix = substr($img,strrpos($img,"."));
        if($imgraw){
            $filename = rand().$subfix;
            file_put_contents(dirname(__FILE__)."/..".$imgdir."/".$filename,$imgraw);
            $content = str_replace($img,"$imgdir$filename",$content);
        }
    }
    return $content;
}

function pycurl($url){
    if(function_exists("curl_init")){
        $ch = curl_init();
        curl_setopt($ch,CURLOPT_URL, $url);
        curl_setopt($ch,CURLOPT_REFERER,"https://images.google.com/");
        curl_setopt($ch,CURLOPT_TIMEOUT,5);
        curl_setopt($ch,CURLOPT_RETURNTRANSFER,true);
        curl_setopt($ch,CURLOPT_USERAGENT,'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)');
        curl_setopt($ch,CURLOPT_SSL_VERIFYPEER, FALSE);
        curl_setopt($ch,CURLOPT_SSL_VERIFYHOST, FALSE);
        $out = curl_exec($ch);
        curl_close($ch);
        return $out;
    }else{
        @ini_set('allow_url_fopen','on');
        return file_get_contents($url);
    }
    return false;
}

//设置文件的发布时间
//参数：每日发布数量，第一篇文章开始时间，每日文章的开始时间，文章时间间隔，文章时间间隔最小位移，文章时间间隔最大唯一
function get_post_date($everydaycount=10,$startdate="2001-01-01",$daystarttime="08:00:00",$interval=1200,$minoffset=10,$maxoffset=100){
    //获取已经发布了多少文章
    if(file_exists(dirname(__FILE__)."/count.txt")){
        $thiscount=file_get_contents(dirname(__FILE__)."/count.txt");
    }else{
        touch(dirname(__FILE__)."/count.txt");
        $thiscount=0;
    }
    //获取这一篇文章距开始的天数
    $thisdate = ceil(($thiscount+1)/$everydaycount);
    //获取这一篇文章距每天一篇的时间
    $thistime= ($thiscount%$everydaycount)*$interval+rand($minoffset,$maxoffset);
    //这一篇文章的位移时间
    $seconds=($thisdate-1)*3600*24+$thistime;
    //这一篇文章的时间戳
    $date = date_create($startdate.' '.$daystarttime);
    return date("Y-m-d H:i:s",date_timestamp_get($date)+$seconds);
}
