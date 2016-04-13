/* lagovskiy.com */

function notice(color, message){
    new jBox('Notice', {
        content: message,
        color: color,
        animation:{open:'slide:bottom',close:'slide:left'},
        attributes:{x:'left',y:'bottom'},
        theme:'NoticeBorder',
    });
}

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


var comment_form = '';
var comment_last = '';

$(document).ready(function() {
    $('#head-menu-link').click(function(){
        $('#head-menu-line').slideToggle();
    });
});