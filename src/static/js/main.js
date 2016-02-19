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


$(document).ready(function() {
    $('#head-menu-link').click(function(){
        $('#head-menu-line').slideToggle();
    });

    $('.dateMask').mask('0000/00/00');
    $('.datetimeMask').mask('0000/00/00 00:00:00');

    $.views.converters({
        datetime: function(value) {
            if ((value == '') || (value == null))
                return value;
            else {
                var date = '/';
                var time = ':';
                if (this.tagCtx.props.date)
                    date = this.tagCtx.props.date;
                if (this.tagCtx.props.time)
                    time = this.tagCtx.props.time;
                var dt = value.split('T');
                var d = dt[0].split('-');
                var t = dt[1].replace('T', '').replace('Z', '').split(':');
                return d[0] + date + d[1] + date + d[2] + ' ' + t[0] + time + t[1] + time + t[2].split('.')[0];
            }
        }
    });

    $.views.tags({
        cutstr: function () {
            var ln = 20;
            var str = this.tagCtx.render();
            if (this.tagCtx.props.max)
                ln = this.tagCtx.props.max;
            if (str.length > ln)
                return  str.substr(0, ln - 1) + "...";
            else
                return str;
        }
    });

});