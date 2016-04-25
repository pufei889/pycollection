<?php
header("content-type:text/html;charset=utf-8");
$username = "admin";
$password = "admin";
$__dir__ = dirname(__FILE__);

if(!isset($_SERVER['PHP_AUTH_USER'])){
    header('WWW-Authenticate: Basic realm="My Realm"');
    header('HTTP/1.0 401 Unauthorized');
    echo 'Text to send if user hits Cancel button';
    exit();
}else if($_SERVER['PHP_AUTH_USER'] != $username ||$_SERVER['PHP_AUTH_PW'] != $password){
    exit("用户名密码错误，请重新输入!");
}

if(isset($_COOKIE['starttime'])){
chdir("..");
if(file_exists("./pycltnd.log")){
echo file_get_contents("./pycltnd.log");
}else{
echo "运行失败!";
}
exit();
}

if(isset($_FILES['key'])){
    $key = $_FILES['key'];
    if($key['type'] != 'text/plain'){
        exit("你只能上传一个文本文件!");
    }
    $u = $_POST['u'];
    $t =  $_POST['t'];
    $c =  $_POST['c'];
    $s = $_POST['s'];
    $newkeyfile = $__dir__."/".time().".txt";
    move_uploaded_file($key['tmp_name'],$newkeyfile);
    chdir("../");
    setcookie("starttime",time(),time()+3600,"/");
    exec("./pycltnd.py -u $u -t $t -c $c $s -k $newkeyfile -d");
    echo "<script>window.location.reload();</script>";
    exit();
}
?>
<!DOCTYPE HTML>
<html lang="zh-cn">
<head>
<meta charset="utf-8">
<title>Cloud Collection API</title>
<style>
* {margin:0;padding:0}
form {width:600px;margin:10px auto;border:1px solid #ccc;box-shadow:5px 5px 5px #eee;border-radius:5px;padding:20px}
input[type='text'] {width:250px;height:25px;line-height:25px;margin-top:10px}
input[type='file'] {width:250px;height:25px;line-height:25px;margin-top:10px}
input[type='submit'] {width:100px;height:25px;line-height:25px;margin-top:10px;display:block;margin:10px auto;cursor:pointer}
select{width:250px;height:25px;line-height:25px;margin-top:10px}
</style>
<head>
<body>
<form method="post" enctype="multipart/form-data">
<label>发布地址:</label><input type="text" name="u" required><br/>
<label>采集间隔:</label><input type="text" name="t" required><br/>
<label>采集条数:</label><select name="c" required><option value="10">10</option><option value="20">20</option><option value="30">30</option></select><br/>
<label>采 集 源:</label><select name="s" requried><option value="getask">ask</option><option value="getbaidu">baidu</option><option value="getbing">bing</option><option value="getcoccoc">coccoc</option><option value="getduckgo">duckgo</option><option value="getecosia">ecosia</option><option value="gethaosou">haosou</option><option value="getizito">izito</option><option value="getlycos">getlycos</option><option value="getsearch">seach</option><option value="getsogou">sogou</option><option value="getwow">wow</option><option value="getyahoo">yahoo</option><option value="getyandex">yandex</option></select><br/>
<label>关键词文件:</lable><input type="file" name="key" required><br/>
<input type="submit" value="开始">
</form>
</body>
