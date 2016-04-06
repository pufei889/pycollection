<?php
//by hito
function showimglist($content){
	$content=trim($content);
	if(substr($content,0,4) != '<h2>') return $content;
	preg_match_all("/<h2>([\s\S\n]*?)<\/p>/i",$content,$match); 
	if(!$match[0]) return $content;
	$content="";  
	foreach($match[0] as $t){
                 preg_match("/<h\d>(.*?)<\/h\d>/i",$t,$m);
                 $alt=strtolower($m[1]);
		$li="<li>".show_rand_img($alt,1,"/images/").$t."</li>";
		$content = $content.$li;
	}
	return "<ul class=\"list\">".$content."</ul>";
}

function show_rand_img($alt="",$num=1,$dir="/images/"){
	$document_root=$_SERVER["DOCUMENT_ROOT"];
	$imgdir=$document_root.$dir;
	if(!file_exists($imgdir)) return;
    $dirarr=array();
    $d = opendir($imgdir);
    while(($file = readdir($d))!== false){
        if($file == ".." || $file==".") continue;
        $type = substr($file,strpos($file,".")+1);
        if($type != "jpg" && $type != "gif" && $type != "png") continue;
        array_push($dirarr,$file);
    }
    closedir($d);
    shuffle($dirarr);
    $html = "";
    for($i = 0 ; $i < $num ; $i++){
        $filename = $dirarr[$i];
		$html .= "<img src=\"$dir$filename\" alt=\"$alt\" class=\"imglist\"/>";
    }
    return $html;
}

//show totle artice
function showarctile($alt,$content,$imgoffset=4,$imgdir="/images/"){
	$content=trim($content);
	if(substr($content,0,4) != '<h2>') return $content;
	preg_match_all("/<h2>([\s\S\n]*?)<\/p>/i",$content,$match); 
	if(!$match[0]) return $content;
	$content = preg_replace("/<h2>[^<>]*<\/h2>/i","",$content);
	$arr=explode('</p>',$content);
	if(count($arr)>$imgoffset){
		$arr[$imgoffset]=$arr[$imgoffset]."\n".show_rand_img($alt,1,$imgdir)."\n";
	}else if(count($arr)>1){
		$arr[0]=$arr[0]."\n".show_rand_img($alt,1,$imgdir)."\n";
	}
	$content=implode('',$arr);
	$content=strip_tags($content,'<img>');
	$content=str_replace("...","",$content);
	return $content;
}
//show just p
function showp($content){
$content=trim($content);
	if(substr($content,0,4) != '<h2>') return $content;
	preg_match_all("/<h2>([\s\S\n]*?)<\/p>/i",$content,$match); 
	if(!$match[0]) return $content;
	$content = preg_replace("/<h2>[^<>]*<\/h2>/i","",$content);
	$content = str_replace("...","",$content);
	return $content;
}
