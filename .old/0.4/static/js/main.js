/* lagovskiy.com */

function isValidEmailAddress(emailAddress) {
    var pattern = /^([a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+(\.[a-z\d!#$%&'*+\-\/=?^_`{|}~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]+)*|"((([ \t]*\r\n)?[ \t]+)?([\x01-\x08\x0b\x0c\x0e-\x1f\x7f\x21\x23-\x5b\x5d-\x7e\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|\\[\x01-\x09\x0b\x0c\x0d-\x7f\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))*(([ \t]*\r\n)?[ \t]+)?")@(([a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\d\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.)+([a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]|[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF][a-z\d\-._~\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]*[a-z\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])\.?$/i;
    return pattern.test(emailAddress);
};

function moveReply(id) {
    if ($('#reply_0').html() != '') {
        comment_form = $('#reply_0').html();
        $('#reply_0').html('');
    }
    if (comment_last != '') {
        $(comment_last).html('');
    }
    $('#reply_' + id).html(comment_form);
    $("#reply_" + id).find("form").find("input[name='parent']").val(id);
    comment_last = '#reply_' + id;
    reloadCaptcha();
}

function reloadCaptcha(){
    var s = $('#comment-image').attr('src');
    $('#comment-image').attr('src', (s.indexOf('?')>0?s.substr(0, s.indexOf('?')):s) + '?' + new Date().getTime());
}

function sendComment(){
   $.ajax({
            type: 'POST',
            url: $('#comment-form').attr('action'),
            data: $('#comment-form').serialize()
        })
        .done(function(data){
            var data_mes = data.split(':')[0];
            var data_code = data.split(':')[1];
            if(data_mes=='ok') {
                $.notify('saved', 'success');
                var id = $('#comment-parent').val();
                $.ajax({
                    url: '/blog/comment/' + data_code
                })
                    .done(function(_data){
                        $('#comment_reply_' + id).html(_data);
                        $('#reply_' + id).html('');
                        location.href = '#comment' + data_code;
                    });
            }
            else {
                $.notify(data_mes, "warn");
            }
        })
        .fail(function(){
            $.notify('data transfer error', 'error');
        });
}


var comment_form = '';
var comment_last = '';

$(document).ready(function() {
    $('#head-menu-link').click(function(){
        $('#head-menu-line').slideToggle();
    });
});