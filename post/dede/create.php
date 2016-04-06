<?php
/* 织梦预约发布接口
 * 附带ping通知百度更新更能
 * author 杨海涛 2014年8月12日
 */
//密码
define("passwd","zg123");
//网站名称
define("webname","锅炉厂");
//织梦库文件
require_once (dirname(__FILE__) . "/include/common.inc.php");
require_once(DEDEINC."/arc.archives.class.php");				  //生成HTML的库文件
//Ping 函数功能
$pinghost="http://ping.baidu.com/ping/RPC2";
$hosts=explode(",",$pinghost);
function rpc_ping($webname,$weburl,$updateurl,$rss){
	if(!function_exists('curl_init')){
		return "推送失败，未开启Curl扩展!";
	}
	global $hosts;
	$xml = <<<EOT
<?xml version="1.0"?>
<methodCall>
  <methodName>weblogUpdates.extendedPing</methodName>
  <params>
	<param>
	  <value><string>$webname</string></value>
	</param>
	<param>
	  <value><string>$weburl</string></value>
	</param>
	<param>
	  <value><string>$updateurl</string></value>
	</param>
	<param>
	  <value><string>$rss</string></value>
	</param>
  </params>
</methodCall>
EOT;
	foreach($hosts as $target){
		$ch = curl_init(); 
		$target=trim($target);
		$header=array("POST".$target."HTTP/1.0","User-Agent: request","Content-Type: text/xml,charset=\"utf-8\"","Content-length:".strlen($xml));
		curl_setopt($ch,CURLOPT_URL,$target); 
		curl_setopt($ch,CURLOPT_POST,1); 
		curl_setopt($ch,CURLOPT_HTTPHEADER,$header);
		curl_setopt($ch,CURLOPT_POSTFIELDS,$xml); 
		ob_start(); 
		curl_exec($ch); 
		curl_close($ch); 
		$result = ob_get_contents(); 
		ob_end_clean();
		if(stristr($result,"<int>0</int>")){
			return "推送成功!";
		}else{
			return "推送失败!";
		}
	}
}
//主体部分
if(!$_GET) exit();
//获取数据
$pass=$_GET["pwd"];//密码
$updated=$_GET["updated"];//已经更新的文章数量
$url=$_GET["url"];//更新的网站
$callback=$_GET["callback"];//回调函数
$ping=$_GET["ping"];		//是否ping
$sitemap=$_GET["sitemap"];	//sitmap地址
//获取没有更新的文章数量
global $dsql;
$row = $dsql->GetOne("select count(id) as count from `#@__archives` where arcrank=-1");
$rest=$row[count];
//返回结果
header("Content-Type:text/javascript");
//密码错误
if($pass!=passwd){
	echo "console.log('$url,密码错误!')";
	exit();
}else{
	//生成html
	$pubdate=time();
	$row = $dsql->GetOne("select id from #@__archives where arcrank=-1 or ismake=0 limit 1");
	$id=$row[id];
	if(empty($id)){
		echo "console.log('全部文章生成完毕!')";
		exit();
	}
	$dsql->ExecuteNoneQuery("update `#@__arctiny` set arcrank=0 where id=$id");
	$dsql->ExecuteNoneQuery("update `#@__archives` set arcrank=0,pubdate=\"$pubdate\" where id=$id");
	$ac=new Archives($id);
	$rurl=$ac->MakeHtml();
	$ac->Close(); 
	if($rurl){
		$rest--;
		$updated++;
		$ping=($ping==0)?"没有推送!":rpc_ping(webname,"http://".$url,"http://".$url.$rurl,"http://".$url.$sitemap);
		echo $callback."('$url','$updated','$rest','$ping');";
	}else{
		echo "console.log('生成HTML失败，请检查权限!')";
		exit();
	}
}
