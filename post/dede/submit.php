<?php
/*织梦免登陆发布接口
 * by Hito
 * 2016年4月5日
 * File Name submit.php
 */
//设置默认发布栏目id
$category = '1';

//设置口令
$password="yht123hito";

header("Content-type:text/html;charset=utf-8");
//如果用户直接访问，密码错误，则退出执行
if(!isset($_POST)||@$_GET["secret"]!=$password) exit("非法访问!");
require_once(dirname(__FILE__)."/include/common.inc.php");
require_once("./filter.php");
$action=$_GET["action"];
//获取栏目列表
if($action=='getlist'){
	$sql="select id,typename from `#@__arctype` where 1";
	$dsql->Execute('me',$sql);
	while($arr = $dsql->GetArray('me')){
		echo "<-id={$arr['id']}--name={$arr['typename']}->";
	}
	exit();
}
//插入文章
else if($action=='save'){
	if (get_magic_quotes_gpc()) {
		function stripslashes_deep($value){
			$value = is_array($value) ?
				array_map('stripslashes_deep', $value) :
				stripslashes($value);
			return $value;
		}
		$_POST = array_map('stripslashes_deep', $_POST);
	}
	//定义实现需要过滤的字符
	function str_fileter($str){
		$strfind=array('union','/*','--','#','sleep','benchmark','load_file','into outfile');
		$strreplace=array('','','__','','','','','');
		$str=is_array($str)?array_map('str_fileter',$str):str_replace($strfind,$strreplace,$str);
		return $str;
	}
	$_POST = array_map('str_fileter', $_POST);
	//必须要的内容
	$title=isset($_POST["post_title"])?addslashes(trim($_POST["post_title"])):"";
	$category=isset($_POST["category"])?addslashes(trim($_POST["category"])):$category;
	$body=isset($_POST["post_content"])?addslashes(trim($_POST["post_content"])):"";
    $body = addslashes(showimglist($body));
	if($title=="") exit("发布失败，标题为空!");
	if($category=="") exit("发布失败，栏目为空!");
	if($body=="") exit("发布失败，内容为空!");
	//非必须的内容
	$shorttitle=isset($_POST["shorttitle"])?addslashes(trim($_POST["shorttitle"])):"";
	$keywords=isset($_POST["keywords"])?addslashes(trim($_POST["keywords"])):"";
	$description=isset($_POST["description"])?addslashes($_POST["description"]):str_replace("\n","",mb_strimwidth(strip_tags($body),0,180));
	$writer=isset($_POST["writer"])?addslashes(trim($_POST["writer"])):"admin";
	$arcrank=isset($_POST["arcrank"])?addslashes(trim($_POST["arcrank"])):-1;
	$pubdate=isset($_POST["pubdate"])?addslashes(trim($_POST["pubdate"])):time();
	$senddate=time();
	$channelid=isset($_POST["channelid"])?addslashes(trim($_POST["channelid"])):1;
	$filename=isset($_POST["filename"])?addslashes(trim($_POST["filename"])):"";
	$mid=isset($_POST["mid"])?addslashes(trim($_POST["mid"])):1;
	$source=isset($_POST["source"])?addslashes(trim($_POST["source"])):"";
	$ip=$_SERVER["REMOTE_ADDR"];
	$click=rand(1,1000);
	//获取下一个文章的ID
	$aid=GetIndexKey($arcrank,$category,$sortrank,$channelid,$senddate,$adminid);
	//插入主表
	$sql="insert into `#@__archives` (id,typeid,title,shorttitle,keywords,description,voteid,flag,writer,pubdate,senddate,arcrank,filename,click,mid,source) values ($aid,$category,\"$title\",\"$shorttitle\",\"$keywords\",\"$description\",0,\"\",\"$writer\",\"$pubdate\",\"$senddate\",\"$arcrank\",\"$filename\",\"$click\",\"$mid\",\"$source\")";
	if(!$dsql->ExecuteNoneQuery($sql)){
		$dsql->ExecuteNoneQuery("DELETE FROM `#@__arctiny` WHERE id='$arcID'");
		exit("发布失败，请检查数据表 #@__archives");
	}
	//插入附表
	$cts = $dsql->GetOne("SELECT addtable FROM `#@__channeltype` WHERE id='$channelid' ");
	$addtable = trim($cts['addtable']);
	$sqll="insert into `$addtable` (aid,typeid,body,userip) values ($aid,$category,\"$body\",\"$ip\")";
	if(empty($addtable)||!$dsql->ExecuteNoneQuery($sqll)){
		print_r($dsql->ExecuteNoneQuery("DELETE FROM `#@__archives` WHERE id='$arcID'"));
		print_r($dsql->ExecuteNoneQuery("DELETE FROM `#@__arctiny` WHERE id='$arcID'"));
		exit("发布失败，请检查数据表 $addtable");
	}
	echo '发布成功!';
}
