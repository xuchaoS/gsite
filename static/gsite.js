$(document).ready(format_json);
$(document).ready(json_code);
function format_json() {
    $('textarea.format_json').each(function (i, o) {
        var o_data = o.value;
        try{
            var j = JSON.parse(o_data);
            o.value = JSON.stringify(j, null, 4);
        }
        catch(err) {
            alert('json格式不正确！！！\n' + err);
        }
    });
}
function json_code() {
    console.log($('code.json_code'))
    $('code.json_code').each(function (i, o) {
        var o_data = o.innerText;
        console.log(o_data)
        var j = JSON.parse(o_data);
        console.log(j)
        o.innerText = JSON.stringify(j, null, 4);
    })
}
