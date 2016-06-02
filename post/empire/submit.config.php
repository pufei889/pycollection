<?php
/*帝国面登陆发布的相关配置
*/
//设置时区
date_default_timezone_set("Asia/Shanghai");
$username = "admin";  //文章发布的用户名，需要改成系统中存在的账户
$_POST['classid'] = "1";  //设置文章发布的栏目ID
$host = "http://localhost/";  //设置网站域名
$sitemap = $host."sitemap.xml"; //设置网站sitemap
$webname = "Powered By https://www.hitoy.org"; //设置网站名称

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


/**请不要改变下面的代码**/
$pinghost = "http://ping.baidu.com/ping/RPC2";
$hosts=explode(",",$pinghost);
function rpc_ping($webname,$weburl,$updateurl,$rss){
	if(!function_exists('curl_init')){
		return "Ping failure, No Curl Extension!";
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
			return "Ping Success!";
		}else{
			return "Ping Failure!";
		}
	}
}

function AddNews($add,$userid,$username){
	global $empire,$class_r,$class_zr,$bclassid,$public_r,$dbtbpre,$emod_r,$host,$sitemap,$webname;
	$add[classid]=(int)$add[classid];
	$userid=(int)$userid;
	if(!$add[title]||!$add[classid])
	{
		//printerror("EmptyTitle","history.go(-1)");
        return "Pushlish Failure, Empty Title";
	}
	//操作权限
	$doselfinfo=CheckLevel($userid,$username,$add[classid],"news");
	if(!$doselfinfo['doaddinfo'])//增加权限
	{
		//printerror("NotAddInfoLevel","history.go(-1)");
        return "Pushlish Failure, No permissions";
	}
	$ccr=$empire->fetch1("select classid,modid,listdt,haddlist,sametitle,addreinfo,wburl,repreinfo from {$dbtbpre}enewsclass where classid='$add[classid]' and islast=1 limit 1");
	if(!$ccr['classid']||$ccr['wburl'])
	{
		//printerror("ErrorUrl","history.go(-1)");
        return "Pushlish Failure, ErrorUrl";
	}
	if($ccr['sametitle'])//验证标题重复
	{
		if(ReturnCheckRetitle($add))
		{
			//printerror("ReInfoTitle","history.go(-1)");
            return "Publish Failure, Title repetition";
	    }
    }
	$add=DoPostInfoVar($add);//返回变量
	$ret_r=ReturnAddF($add,$class_r[$add[classid]][modid],$userid,$username,0,0,1);//返回自定义字段
	$newspath=FormatPath($add[classid],$add[newspath],1);//查看目录是否存在，不存在则建立
	//审核权限
	if(!$doselfinfo['docheckinfo'])
	{
		$add['checked']=$class_r[$add[classid]][checked];
	}
	//必须审核
	if($doselfinfo['domustcheck'])
	{
		$add['checked']=0;
	}
	//推荐权限
	if(!$doselfinfo['dogoodinfo'])
	{
		$add['isgood']=0;
		$add['firsttitle']=0;
		$add['istop']=0;
	}
	//签发
	$isqf=0;
	if($class_r[$add[classid]][wfid])
	{
		$add[checked]=0;
		$isqf=1;
	}
	$newstime=empty($add['newstime'])?time():to_time($add['newstime']);
	$truetime=time();
	$lastdotime=$truetime;
	//是否生成
	$havehtml=0;
	if($add['checked']==1&&$ccr['addreinfo'])
	{
		$havehtml=1;
	}
	//返回关键字组合
	if($add['info_diyotherlink'])
	{
		$keyid=DoPostDiyOtherlinkID($add['info_keyid']);
	}
	else
	{
		$keyid=GetKeyid($add[keyboard],$add[classid],0,$class_r[$add[classid]][link_num]);
	}
	//附加链接参数
	$addecmscheck=empty($add['checked'])?'&ecmscheck=1':'';
	//索引表
	$sql=$empire->query("insert into {$dbtbpre}ecms_".$class_r[$add[classid]][tbname]."_index(classid,checked,newstime,truetime,lastdotime,havehtml) values('$add[classid]','$add[checked]','$newstime','$truetime','$lastdotime','$havehtml');");
	$id=$empire->lastid();
	$pubid=ReturnInfoPubid($add['classid'],$id);
	$infotbr=ReturnInfoTbname($class_r[$add[classid]][tbname],$add['checked'],$ret_r['tb']);
	//主表
	$infosql=$empire->query("insert into ".$infotbr['tbname']."(id,classid,ttid,onclick,plnum,totaldown,newspath,filename,userid,username,firsttitle,isgood,ispic,istop,isqf,ismember,isurl,truetime,lastdotime,havehtml,groupid,userfen,titlefont,titleurl,stb,fstb,restb,keyboard".$ret_r['fields'].") values('$id','$add[classid]','$add[ttid]','$add[onclick]',0,'$add[totaldown]','$newspath','$filename','$userid','".addslashes($username)."','$add[firsttitle]','$add[isgood]','$add[ispic]','$add[istop]','$isqf',0,'$add[isurl]','$truetime','$lastdotime','$havehtml','$add[groupid]','$add[userfen]','".addslashes($add[my_titlefont])."','".addslashes($add[titleurl])."','$ret_r[tb]','$public_r[filedeftb]','$public_r[pldeftb]','".addslashes($add[keyboard])."'".$ret_r['values'].");");
	//副表
	$finfosql=$empire->query("insert into ".$infotbr['datatbname']."(id,classid,keyid,dokey,newstempid,closepl,haveaddfen,infotags".$ret_r['datafields'].") values('$id','$add[classid]','$keyid','$add[dokey]','$add[newstempid]','$add[closepl]',0,'".addslashes($add[infotags])."'".$ret_r['datavalues'].");");
	//更新栏目信息数
	AddClassInfos($add['classid'],'+1','+1',$add['checked']);
	//更新新信息数
	DoUpdateAddDataNum('info',$class_r[$add['classid']]['tid'],1);
	//签发
	if($isqf==1)
	{
		InfoInsertToWorkflow($id,$add[classid],$class_r[$add[classid]][wfid],$userid,$username);
	}
	//更新附件表
	UpdateTheFile($id,$add['filepass'],$add['classid'],$public_r['filedeftb']);
	//取第一张图作为标题图片
	if($add['getfirsttitlepic']&&empty($add['titlepic']))
	{
		$firsttitlepic=GetFpicToTpic($add['classid'],$id,$add['getfirsttitlepic'],$add['getfirsttitlespic'],$add['getfirsttitlespicw'],$add['getfirsttitlespich'],$public_r['filedeftb']);
		if($firsttitlepic)
		{
			$addtitlepic=",titlepic='".addslashes($firsttitlepic)."',ispic=1";
		}
	}
	//文件命名
	if($add['filename'])
	{
		$filename=$add['filename'];
	}
	else
	{
		$filename=ReturnInfoFilename($add[classid],$id,'');
	}
	//信息地址
	$updateinfourl='';
	if(!$add['isurl'])
	{
		$infourl=GotoGetTitleUrl($add['classid'],$id,$newspath,$filename,$add['groupid'],$add['isurl'],$add['titleurl']);
		$updateinfourl=",titleurl='$infourl'";
	}
	$usql=$empire->query("update ".$infotbr['tbname']." set filename='$filename'".$updateinfourl.$addtitlepic." where id='$id'");
	//替换图片下一页
	if($add['repimgnexturl'])
	{
		UpdateImgNexturl($add[classid],$id,$add['checked']);
	}
	//投票
	AddInfoVote($add['classid'],$id,$add);
	//加入专题
	InsertZtInfo($add['ztids'],$add['zcids'],$add['oldztids'],$add['oldzcids'],$add['classid'],$id,$newstime);
	//TAGS
	if($add[infotags]&&$add[infotags]<>$add[oldinfotags])
	{
		eInsertTags($add[infotags],$add['classid'],$id,$newstime);
	}
	//增加信息是否生成文件
	if($ccr['addreinfo']&&$add['checked'])
	{
		GetHtml($add['classid'],$id,'',0);
	}
	//生成上一篇
	if($ccr['repreinfo']&&$add['checked'])
	{
		$prer=$empire->fetch1("select * from {$dbtbpre}ecms_".$class_r[$add[classid]][tbname]." where id<$id and classid='$add[classid]' order by id desc limit 1");
		GetHtml($add['classid'],$prer['id'],$prer,1);
	}
	//生成栏目
	if($ccr['haddlist']&&$add['checked'])
	{
		hAddListHtml($add['classid'],$ccr['modid'],$ccr['haddlist'],$ccr['listdt']);//生成信息列表
		if($add['ttid'])//生成标题分类列表
		{
			ListHtml($add['ttid'],'',5);
		}
	}
	//同时发布
	$copyclassid=$add[copyclassid];
	$cpcount=count($copyclassid);
	if($cpcount)
	{
		$copyids=AddInfoToCopyInfo($add[classid],$id,$copyclassid,$userid,$username,$doselfinfo);
		if($copyids)
		{
			UpdateInfoCopyids($add['classid'],$id,$copyids);
		}
	}
	if($sql)
	{
		//返回地址
		if($add['ecmsfrom']&&(stristr($add['ecmsfrom'],'ListNews.php')||stristr($add['ecmsfrom'],'ListAllInfo.php')))
		{
			$ecmsfrom=$add['ecmsfrom'];
		}
		else
		{
			$ecmsfrom=$add['ecmsnfrom']==1?"ListNews.php?bclassid=$add[bclassid]&classid=$add[classid]":"ListAllInfo.php?tbname=".$class_r[$add[classid]][tbname];
			$ecmsfrom.=hReturnEcmsHashStrHref2(0);
		}
		$GLOBALS['ecmsadderrorurl']=$ecmsfrom.$addecmscheck;
		insert_dolog("classid=$add[classid]<br>id=".$id."<br>title=".$add[title],$pubid);//操作日志
		//printerror("AddNewsSuccess","AddNews.php?enews=AddNews&ecmsnfrom=$add[ecmsnfrom]&bclassid=$add[bclassid]&classid=$add[classid]".$addecmscheck.hReturnEcmsHashStrHref2(0));
        $url = $add['isurl']?$add['isurl']:str_replace("//","/",$host.$infourl);
        $pingresult = rpc_ping($webname,$host,$url,$sitemap);
        return "Publish Success, ".$pingresult;
	}
	else
	{
		//printerror("DbError","");
        return "Publish Failure, DataBases Error";
	}
}
//增加信息处理变量
function DoPostInfoVar($add){
	global $class_r;
	//组合标题属性
	$add[titlecolor]=RepPhpAspJspcodeText($add[titlecolor]);
	$add['my_titlefont']=TitleFont($add[titlefont],$add[titlecolor]);
	//专题
	$add['ztids']=RepPostVar($add['ztids']);
	$add['zcids']=RepPostVar($add['zcids']);
	$add['oldztids']=RepPostVar($add['oldztids']);
	$add['oldzcids']=RepPostVar($add['oldzcids']);
	//其它变量
	$add[keyboard]=RepPhpAspJspcodeText(DoReplaceQjDh($add[keyboard]));
	$add[titleurl]=RepPhpAspJspcodeText($add[titleurl]);
	$add[checked]=(int)$add[checked];
	$add[istop]=(int)$add[istop];
	$add[dokey]=(int)$add[dokey];
	$add[isgood]=(int)$add[isgood];
	$add[groupid]=(int)$add[groupid];
	$add[newstempid]=(int)$add[newstempid];
	$add[firsttitle]=(int)$add[firsttitle];
	$add[userfen]=(int)$add[userfen];
	$add[closepl]=(int)$add[closepl];
	$add[ttid]=(int)$add[ttid];
	$add[oldttid]=(int)$add[oldttid];
	$add[onclick]=(int)$add[onclick];
	$add[totaldown]=(int)$add[totaldown];
	$add[infotags]=RepPhpAspJspcodeText(DoReplaceQjDh($add[infotags]));
	$add[ispic]=$add[titlepic]?1:0;
	$add[filename]=RepFilenameQz($add[filename],1);
	$add[newspath]=RepFilenameQz($add[newspath],1);
	$add['isurl']=$add['titleurl']?1:0;
	return $add;
}

//增加投票
function AddInfoVote($classid,$id,$add){
	global $empire,$dbtbpre,$class_r;
	$pubid=ReturnInfoPubid($classid,$id);
	$num=$empire->gettotal("select count(*) as total from {$dbtbpre}enewsinfovote where pubid='$pubid' limit 1");
	$votename=$add['vote_name'];
	$votenum=$add['vote_num'];
	//统计总票数
	for($i=0;$i<count($votename);$i++)
	{
		$t_votenum+=$votenum[$i];
	}
	$t_votenum=(int)$t_votenum;
	$voteclass=(int)$add['vote_class'];
	$width=(int)$add['vote_width'];
	$height=(int)$add['vote_height'];
	$doip=(int)$add['dovote_ip'];
	$tempid=(int)$add['vote_tempid'];
	$add['vote_title']=hRepPostStr($add['vote_title'],1);
	$add['vote_dotime']=hRepPostStr($add['vote_dotime'],1);
	//附加字段
	$diyotherlink=(int)$add['info_diyotherlink'];
	$infouptime=0;
	if($add['info_infouptime'])
	{
		$infouptime=to_time($add['info_infouptime']);
	}
	$infodowntime=0;
	if($add['info_infodowntime'])
	{
		$infodowntime=to_time($add['info_infodowntime']);
	}
	if($num)	//修改
	{
		$votetext=ReturnVote($add['vote_name'],$add['vote_num'],$add['delvote_id'],$add['vote_id'],1);	//返回组合
		$votetext=hRepPostStr($votetext,1);
		$sql=$empire->query("update {$dbtbpre}enewsinfovote set title='$add[vote_title]',votenum='$t_votenum',votetext='$votetext',voteclass='$voteclass',doip='$doip',dotime='$add[vote_dotime]',tempid='$tempid',width='$width',height='$height',diyotherlink='$diyotherlink',infouptime='$infouptime',infodowntime='$infodowntime' where pubid='$pubid' limit 1");
	}
	else	//增加
	{
		$votetext=ReturnVote($add['vote_name'],$add['vote_num'],$add['delvote_id'],$add['vote_id'],0);	//返回组合
		if(!($votetext||$diyotherlink||$infouptime||$infodowntime))
		{
			return '';
		}
		$votetext=hRepPostStr($votetext,1);
		$sql=$empire->query("insert into {$dbtbpre}enewsinfovote(pubid,id,classid,title,votenum,voteip,votetext,voteclass,doip,dotime,tempid,width,height,diyotherlink,infouptime,infodowntime,copyids) values('$pubid','$id','$classid','$add[vote_title]','$t_votenum','','$votetext','$voteclass','$doip','$add[vote_dotime]','$tempid','$width','$height','$diyotherlink','$infouptime','$infodowntime','');");
	}
}
