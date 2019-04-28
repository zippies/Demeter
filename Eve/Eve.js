/**
 * Created by cc on 2017/7/18.
 */


baseUrl = "http://eve.host";
// baseUrl = "http://localhost:8888";

// 获取元素xpath全路径
function getXpath(xpaths, deepth, ele){
    tagname = ele.tagName.toLowerCase();
    index = 1;
    while(true){  // 找到元素在父元素内是第几个
        if($(ele).prev().length != 0){  // 判断在当前元素前是否有同级元素
            if($(ele).prev()[0].tagName.toLowerCase() == tagname){  // 如果有，并且tagname相同，则index + 1
                index = index + 1
            }
            ele = $(ele).prev()[0]
        }else{  // 如果当前元素前没有同级元素，则将当前元素赋值为父元素，跳出循环，继续递归
            ele = $(ele).parent()[0];
            break
        }
    }

    xpaths[deepth] = tagname+"["+index+"]";
    deepth = deepth + 1;
    if (tagname == "html"){
        return xpaths
    }else{
        return getXpath(xpaths, deepth, ele)
    }
}


function healthCheck(){
    // 每次加载页面时，将页面dom传至后台，后台根据url 搜索出当前页面库里已录入的所有元素，遍历元素，对元素xpath进行健康检查，
    // 若xpath检查不存在，标记元素生病，汇总生病元素，返回前台，前台根据提示修复生病元素，直到当前页面所有元素被修复

    $.ajax({
        url: baseUrl + "/health_check",
        type: "post",
        data: {
            page_url: unescape(escape(document.URL)),
            page_body: document.body.innerHTML
        },
        error: function(req){
            layer.msg(req.status);
        },
        success: function(data){
            data = JSON.parse(data);
            if(data.code == 1){
                sessionStorage.sick_elements = data.content
            }else{
                layer.msg("当前页面元素均健康！");
                sessionStorage.removeItem("sick_elements")
            }
        }
    });

    if(sessionStorage.sick_elements){
        layer.open({
            type: 1,
            title: "元素健康检测",
            maxmin: true,
            shade: false,
            shadeClose: true,
            area: ['350px', '150px'], //宽高
            offset: '0px',
            content: sessionStorage.sick_elements
        });
    }
    console.log("health check done.");
}

function getElementInfo(ele){
    var xpaths = [];
    // 使用js解析出元素的xpath全路径
    xpath = getXpath(xpaths, 0, $(ele)[0]).reverse().join("/");
    console.log("xpath:", xpath);
    // 使用元素的xpath全路径和当前页面的html内容请求后台服务接口，接口判断元素是否已被保存，并返回判断结果
    $.ajax({
        url: baseUrl + "/get_element_by_xpath",
        type: "post",
        data: {
            page_url: unescape(escape(document.URL)),
            xpath: xpath,
            page_body: document.body.innerHTML
        },
        error: function(req, textStatus){
            layer.msg("EverServer未启动或插件被拦截");
            return null
        },
        success: function(data){
            element_info = JSON.parse(data);
            if (element_info.length == 0){
                element_info = [{
                    name: "",
                    page_url: ""
                }]
            }
            // 在插件弹框并显示元素的保存状态
            showElementInfo(xpath, element_info)
        }
    })
}

function showElementInfo(xpath, element_info){
    console.log("saved_name_value", element_info[0].name);
    console.log("name_pre_value", localStorage.name_pre_value);
    console.log("url_pre_value", localStorage.url_pre_value);
    url_value = document.URL;
    element_url = element_info[0].page_url.split("/").join("\\/")
    if(eval("/"+ element_url +"/.test(document.URL)") && eval("/" + element_url + "/.test(localStorage.url_pre_value)")){
        url_value = localStorage.url_pre_value
    }
    console.log("url_value", url_value);
    tmpstr = nunjucks.renderString(
        info_template,
        {
            xpath: xpath,
            baseUrl: baseUrl,
            url_value: url_value,
            saved_name_value: element_info[0].name,
            name_pre_value: localStorage.name_pre_value
        }
    );

    layer.closeAll();

    layer.open({
        type: 1,
        shade: false,
        title: false,
        shift: 5,
        closeBtn: 1,
        area: [window.screen.width + "px", window.screen.height / 5 + "px"], //宽高
        offset: window.screen.height / 5 * 3 + "px",
        content: tmpstr
    });
}

document.body.style.border = "1px solid purple";
var underclearobj;

document.onmousedown=function(event){
    // 获取被点击元素
    element = event.target || event.srcElement;

    var layerClassList = ["addon", "layui-layer-content", "layui-layer-title", "layui-layer-close", "layui-layer-btn", "layui-layer-btn0", "layui-layer-btn1"];
    var isaddon = false;
    // 判断是否是插件元素
    layerClassList.forEach(function(classname){
        if($(element).hasClass(classname) || $(element).parent().parent().parent().parent().parent().hasClass(classname) || $(element).parent().parent().parent().hasClass(classname) ||$(element).parent().parent().parent().parent().hasClass(classname)){
            isaddon = true;
            return false;
        }
    });
    // 如果不是插件弹框则给元素标记红框
    if(!isaddon){
        if(underclearobj){
            underclearobj.style.border = "";
        }
        underclearobj = element;
        element.style.border = "1px solid red";
        $(element).css({"border-radius":"2px","-webkit-border-radius":"2px"});
        // 向后台服务发送请求，获取元素在后台系统中的保存信息
        getElementInfo(element)
    }
};

document.onkeydown = function(e){
    if (e.which === 27) {
        layer.closeAll()
    }

    if (e.metaKey && e.keyCode == 75){ // command + k
        healthCheck();
    }
};


info_template = `
<script>

function createXHR(){
	if(typeof XMLHttpRequest != "undefined"){ // 非IE6浏览器
		return new XMLHttpRequest();
	}else if(typeof ActiveXObject != "undefined"){   // IE6浏览器
		var version = [
			"MSXML2.XMLHttp.6.0",
			"MSXML2.XMLHttp.3.0",
			"MSXML2.XMLHttp",
		];
		for(var i = 0; i < version.length; i++){
			try{
				return new ActiveXObject(version[i]);
			}catch(e){
			}
		}
	}else{
		throw new Error("您的系统或浏览器不支持XHR对象！");
	}
}

function ajax(obj){
	var xhr = createXHR();

	if(obj.async === true){
		xhr.onreadystatechange = function(){
			if(xhr.readyState == 4){
				callBack();
			}
		}
	}

	xhr.open(obj.method, obj.url, obj.async);

	if(obj.method === "post"){
		xhr.send(obj.data);
	}else{
		xhr.send(null);
	}

	if(obj.async === false){
		callBack();
	}

	function callBack(){
		if(xhr.status == 200){
			obj.success(xhr.responseText);
		}else{
			obj.Error("Status:"+xhr.status+" ErrorMsg:"+xhr.statusText);
		}
	}
}


$("#saveElement").click(function(){
	formdata = new FormData(document.getElementById("newelementform"));
	formdata.append("page_body", JSON.stringify(document.body.innerHTML).replace("\\n", ""));
	name = $("#elementname").val();
	url = $("#url_value").val();
	islegal = /([\u4e00-\u9fa5a-zA-Z0-9]+_){2,}[\u4e00-\u9fa5a-zA-Z0-9]+/.test(name)
	if(!islegal){
	    layer.msg("格式不正确(例:登录页面_登录功能_用户名输入框)");
	    return
	}
	if(!$("#url_value").val()||!$("#xpath_value").val()){
	    layer.msg("元素信息不能为空");
	    if(!$("#url_value").val()){
	        $("#url_value").focus();
	    }else{
	        $("#xpath_value").focus();
	    }
	    return
	}
	
    ajax({
        "method": "post",
        "url": "{{ baseUrl }}/save",
        "data": formdata,
        "async": false,
        "success": function(data){
            data = JSON.parse(data)
            if(data.code == 0){
                localStorage.name_pre_value = name;
                localStorage.url_pre_value = url;
                layer.msg("保存成功！")
            }else if(data.code == 1){
                index = layer.confirm('检测到相同的元素命名，是否覆盖？',{
                    btn: ['取消', '确定']
                }, function(){
                    layer.close(index)
                },function(){
                    ajax({
                        "method": "post",
                        "url": "{{ baseUrl }}/save?force=true",
                        "data": formdata,
                        "async": false,
                        "success": function(data){
                            data = JSON.parse(data)
                            if(data.code == 0){
                                localStorage.name_pre_value = name;
                                localStorage.url_pre_value = url;
                                layer.msg("保存成功！")
                            }else{
                                layer.msg("保存失败！"+data.errorMsg)
                            }
                        },
                        "Error": function(text){
                            layer.msg("error:"+text)
                        }
                    });
                })
            }else{
                layer.msg("保存失败！" + data.errorMsg)
            }
        },
        "Error": function(text){
            layer.msg("error:"+text)
        }
    });
})

</script>

<div class="addon" style="width:95%;padding:10px">
	<div class="addon col-lg-12">
	    <form class="addon form-inline" id="newelementform" action="{{ baseUrl }}/save" method="post">
	        <div class="addon col-lg-6">
                <div class="addon input-group" style="width:100%">
                    <span class="addon input-group-addon" id="basic-addon" style="width:15%;text-align:left">所属页面url</span>
                    <input type="text" class="addon form-control" id="url_value" name="url_value" value="{{ url_value }}" aria-describedby="basic-addon" required>
                </div>
            </div>
            <div class="addon col-lg-4" style="display:none">
                <div class="addon input-group" style="width:100%">
                    <span class="addon input-group-addon" id="basic-addon1" style="width:15%;text-align:left">xpath</span>
                    <input type="text" class="addon form-control" id="xpath_value" name="xpath_value" value="{{ xpath }}" aria-describedby="basic-addon1" required>
                </div>
            </div>
            <div class="addon col-lg-4">
                    <div class="addon input-group">
                        <span class="addon input-group-addon" id="basic-addon2" style="width:15%;text-align:left">命名元素</span>
                        <input type="text" id="elementname" name="elementname" class="addon form-control" placeholder="系统名_模块名_功能名_元素名" aria-describedby="basic-addon2" value="{% if saved_name_value %}{{ saved_name_value }}{% else %}{{ name_pre_value }}{% endif %}" onKeyUp="value=value.replace(/-/g,'_')" required>
                    </div>
            </div>
            <div class="addon col-lg-2">
                <a class="addon btn btn-default" id="saveElement">保存元素</a> <span class="label {% if saved_name_value %}label-success">已保存{% else %}label-danger">未保存{% endif %}</span>
            </div>
		</form>
	<div>
		<div style="margin-top:5px"></div>
		<div style="text-align:center">
如果页面url中存在可变参数，需要将可变参数替换成<code>{var}</code>；<code>{all}</code>用来替换任意长度的字符<br>
例如: http://xxxx/table?id=<code>0</code>&action=new<br>
改成: http://xxxx/table?id=<code>{var}</code>&action=new<br>
<a href="{{ baseUrl }}" target="_blank">查看已有元素</a>
		</div>
</div>
`;