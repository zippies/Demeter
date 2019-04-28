/**
 * Created by chaochen on 2017/7/18.
 */

$(function(){
    var elementdata;
    baseUrl = "http://eve.host";
    $.ajax({
        type: "get",
        url: baseUrl + "/elements",
        async: false,
        success: function(data){
            elementdata = JSON.parse(data)
        },
        error: function(req){
            layer.msg("error:"+req.status, { offset: '50px'})
        }
    });

    $("#elementtable").bootstrapTable({
        pagination: true,
        pageNumber: 1,
        pageSize: 20,
        search: true,
        searchAlign: 'left',
        striped: true,
        clickToSelect: true,
        columns: [
            {
                field: 'name',
                width: '30%',
                title: 'ElementName'
            }, {
                field: 'by',
                width: '10%',
                title: 'FindBy'
            },{
                field: 'value',
                width: '30%',
                title: 'ElementValue'
            },{
                field: 'page_url',
                width: '15%',
                title: 'PagePath'
            },{
                field: 'operate',
                width: '15%',
                title: 'operate'
            }
        ],
        data: elementdata
    });
});


function save(){
    id = $(this).attr("id").split("save_")[1];
    name = document.getElementById("name_" + id).value;
    findby = document.getElementById("findby_" + id).value;
    value = document.getElementById("value_" + id).value;
    page_url = document.getElementById("page_url_" + id).value;
    if(name && findby && value && page_url){
        $.ajax({
            url: baseUrl + "/saveedit/" + id,
            data: {"name": name, "findby": findby, "value": value, "page_url": page_url},
            type: "post",
            async: true,
            error: function(request){
                layer.msg("请求失败！"+request.status, { offset: '50px'})
            },
            success: function(data){
                data = JSON.parse(data);
                if(data.code == 0){
                    layer.msg("保存成功！", { offset: '50px'});
                }else{
                    layer.msg("保存失败！" + data.errorMsg, { offset: '50px'})
                }
            }
        })
    }else{
        layer.msg("ElementName/FindBy/ElementValue/PageUrl 不允许为空", { offset: '50px'})
    }
}

function del(){
    id = $(this).attr("id").split("del_")[1];
    layer.confirm(
        "确认删除吗?",
        { btn: ['确认','取消'], offset: '50px' },
        function(){
            $.ajax({
                url: baseUrl + "/delelement/" + id,
                type: "get",
                async: true,
                error: function(request){
                    layer.msg(request.status)
                },
                success: function(data){
                    data = JSON.parse(data);
                    if(data.result){
                        layer.msg("删除成功", { offset: '50px'});
                        window.location.reload();
                    }else{
                        layer.msg("删除失败:"+data.errorMsg, { offset: '50px'})
                    }
                }
            })
        },
        function(){
            layer.closeAll()
        }
    );
}

document.onmousedown=function(event) {
    saves = document.getElementsByClassName("save");
    dels = document.getElementsByClassName("del");
    save_args = Array.prototype.slice.call(saves);
    del_args = Array.prototype.slice.call(dels);
    save_args.forEach(function(ele){
        ele.addEventListener("click", save);
    });
    del_args.forEach(function(ele){
        ele.addEventListener("click", del);
    })
};
