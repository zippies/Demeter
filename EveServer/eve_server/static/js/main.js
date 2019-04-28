/**
 * Created by chaochen on 2017/7/18.
 */

$(function(){
    freshTable()
});

function freshTable(){
    var elementdata;
    $.ajax({
        type: "get",
        url: "/elements",
        async: false,
        success: function(data){
            elementdata = JSON.parse(data)
        },
        error: function(req){
            layer.msg("error:"+req.status)
        }
    });

    $("#elementtable").bootstrapTable('destroy').bootstrapTable({
        pagination: true,
        pageNumber: 1,
        pageSize: 20,
        search: true,
        searchAlign: 'left',
        showRefresh: true,
        striped: true,
        searchText: sessionStorage.searchtext,
        clickToSelect: true,
        columns: [
            {
                field: 'name',
                width: '23%',
                title: 'ElementName'
            }, {
                field: 'by',
                width: '7%',
                title: 'FindBy'
            },{
                field: 'value',
                width: '30%',
                title: 'ElementValue'
            },{
                field: 'page_url',
                width: '25%',
                title: 'PageUrlPattern'
            },{
                field: 'is_used',
                width: '5',
                title: 'isUsed'
            },{
                field: 'operate',
                width: '10%',
                title: 'operate'
            }
        ],
        onSearch: function (text) {
            sessionStorage.searchtext = text;
        },
        data: elementdata
    });

}

function add(){
    $.ajax({
        url: "/save?eve=true",
        type: "post",
        data: $("#add-form").serialize(),
        error: function(req){
            layer.msg(req.status)
        },
        success: function(data){
            data = JSON.parse(data);
            if(data.code == 0){
                layer.msg("保存成功！");
                freshTable()
            }else{
                layer.msg("保存失败！" + data.errorMsg)
            }
        }
    })
}


function save(){
    id = $(this).attr("id").split("save_")[1];
    name = document.getElementById("name_" + id).value;
    findby = document.getElementById("findby_" + id).value;
    value = document.getElementById("value_" + id).value;
    page_url = document.getElementById("page_url_" + id).value;
    if(name && findby && value && page_url){
        $.ajax({
            url: "/saveedit/" + id,
            data: {"name": name, "findby": findby, "value": value, "page_url": page_url},
            type: "post",
            async: true,
            error: function(request){
                layer.msg("请求失败！"+request.status)
            },
            success: function(data){
                data = JSON.parse(data);
                if(data.code == 0){
                    layer.msg("保存成功！");
                }else{
                    layer.msg("保存失败！" + data.errorMsg)
                }
            }
        })
    }else{
        layer.msg("ElementName/FindBy/ElementValue/PageUrl 不允许为空")
    }
}

function del(){
    id = $(this).attr("id").split("del_")[1];
    layer.confirm(
        "确认删除吗?",
        { btn: ['确认','取消']},
        function(){
            $.ajax({
                url: "/delelement/" + id,
                type: "get",
                async: true,
                error: function(request){
                    layer.msg(request.status)
                },
                success: function(data){
                    data = JSON.parse(data);
                    if(data.result){
                        layer.msg("删除成功");
                        freshTable()
                    }else{
                        layer.msg("删除失败:"+data.errorMsg)
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
