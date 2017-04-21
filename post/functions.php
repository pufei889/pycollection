<?php
function rand_get_dir_image($dir){
    $tmp=array();
    if($dd = opendir($dir)){
        while(($file=readdir($dd)) !== false){
            if($file == "." || $file == "..") continue;
            array_push($tmp,$file);
        }
    closedir($dd);
    shuffle($tmp);
        if(count($tmp)>0)
            return $tmp[0];
        return false;
    }
    return false;
}

function list_add_thumb($content){
    preg_match_all("/(<h2>([^>]*)<\/h2>)[\s\r\n]*(<p>[^>]*<\/p>)/",$content,$match);
   if(empty($match[1])) return $content;
    $content = "";
    for($i=0;$i<count($match[1]);$i++){
        $title = $match[1][$i]."\r\n";
        $no_tag_title =$match[2][$i];
        $desc = $match[3][$i]."\r\n";
        $img = "<img src=\"/images/".rand_get_dir_image("./images/")."\" alt=\"$no_tag_title\" class=\"thumb_list\">\r\n";
        $content .= $img.$title.$desc;
    }
   return $content; 
}

add_filter("the_content","list_add_thumb");
