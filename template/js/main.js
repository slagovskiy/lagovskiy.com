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
