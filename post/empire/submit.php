<?php
if(!isset($_GET['secret']) || $_GET['secret'] != 'yht123hito') exit("Publish failed, password error!");
define('EmpireCMSAdmin','1');
require("./submit.config.php");
require("../class/connect.php");
require("../class/db_sql.php");
require("../class/functions.php");
require LoadLang("pub/fun.php");
require("../class/delpath.php");
require("../class/copypath.php");
require("../class/t_functions.php");
require("../data/dbcache/class.php");
require("../data/dbcache/MemberLevel.php");
if(isset($_GET['action'])&&$_GET['action'] == "list"){
    $cates = array();
    $i = 0;
    foreach($class_r as $kv)
    {
        if($kv['modid']=='1')
        {
            $cates[$i]=array('cname'=>$kv['classname'],'cid'=>$kv['classid'],'pid'=>$kv['bclassid']);
            $i++;
        }
    }
    foreach($cates as $v){
        echo "<<<".$v['cid']."--".$v['cname'].">>>";
    }
    exit();
}
if(!isset($_GET['action']) || $_GET['action'] != "save" || !isset($_POST)) exit("Prohibited"); 
$link=db_connect();
$empire=new mysqlquery();
$lur=$empire->fetch1("select * from {$dbtbpre}enewsuser where `username`='$username'");
if(!$lur) exit('Publish failed, user'.$loginin.' does not exists!');
$logininid=$lur['userid'];
$loginrnd=$lur['rnd'];
$loginlevel=$lur['groupid'];
$loginadminstyleid=$lur['adminstyleid'];
$incftp=0;
if($public_r['phpmode']){
    include("../class/ftp.php");
    $incftp=1;
}
$navtheid=(int)$_POST['filepass'];
echo AddNews($_POST,$logininid,$loginin);
db_close();
$empire=null;
