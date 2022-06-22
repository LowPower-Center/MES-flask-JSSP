function getData(url) {
var data = "";
    $.ajax({
        type: "GET",//POST方式提交
        dataType: "json",//返回json类型
        url: url ,//请求url
        async:false,//同步
        success: function (result) {
            data =  result;
        },
    });
    return data
}