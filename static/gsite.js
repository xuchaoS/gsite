$(document).ready(format_json);
$(document).ready(json_code);
$(document).ready(disable_form);

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
    $('code.json_code').each(function (i, o) {
        var o_data = o.innerText;
        var j = JSON.parse(o_data);
        o.innerText = JSON.stringify(j, null, 4);
    })
}
function disable_form() {
    $('form.disabled input:not(:hidden)').each(function (i, o) {
        o.disabled = true;
    });
    $('form.disabled textarea:not(:hidden)').each(function (i, o) {
        o.disabled = true;
    });
}
