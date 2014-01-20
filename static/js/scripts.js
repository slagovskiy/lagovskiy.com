function isValidEmailAddress(emailAddress)
{
    var pattern = new RegExp(/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i);
    return pattern.test(emailAddress);
}


function validateCommentForm(item)
{
    var e;
    var ret = true;
    e = item.find('#comment_capcha');
    if(e.val()=='')
    {
        e.css({backgroundColor: '#f2dede'});
        ret = false;
    }
    else
    {
        $.ajax({
            url: '/capcha_check/' + e.val() + '/',
            cache: false,
            async: false,
            success: function(data){
                if (data=='1')
                {
                    e.css({backgroundColor: ''});
                    ret = true;
                }
                else
                {
                    e.css({backgroundColor: '#f2dede'});
                    ret = false;
                }
            },
            error: function(e, xhr){
                e.css({backgroundColor: '#f2dede'});
                ret = false;
                msg_error("Error", "check capcha");
            }
        });
    }
    e = item.find('#comment_content');
    if (e.val()=='')
    {
        e.css({backgroundColor: '#f2dede'});
        ret = false;
    }
    else
    {
        e.css({backgroundColor: ''});
    }
    e = item.find('#comment_name');
    if(e.val()=='')
    {
        e.css({backgroundColor: '#f2dede'});
        ret = false;
    }
    else
    {
        e.css({backgroundColor: ''});
    }
    e = item.find('#comment_email');
    if(e.val()!='')
    {
        if (!isValidEmailAddress(e.val()))
        {
            e.css({backgroundColor: '#f2dede'});
            ret = false;
        }
        else
        {
            e.css({backgroundColor: ''});
        }
    }
    else
    {
        e.css({backgroundColor: ''});
    }

    if(item.find('input[name=comment_subscribe]').prop('checked'))
    {
        if(e.val()=='')
        {
            e.css({backgroundColor: '#f2dede'});
            ret = false;
        }
         else
        {
            if (!isValidEmailAddress(e.val()))
            {
                e.css({backgroundColor: '#f2dede'});
                ret = false;
            }
            else
            {
                e.css({backgroundColor: ''});
            }
        }
   }
    return ret;
}

function imageForTrue(item)
{
    if(item=='True')
    {
        return '<i class="glyphicon glyphicon-ok-sign"></i>';
    }
    else
    {
        return '';
    }
}

String.prototype.hashCode = function(){
    var hash = 0, i, char;
    if (this.length == 0) return hash;
    for (i = 0, l = this.length; i < l; i++) {
        char  = this.charCodeAt(i);
        hash  = ((hash<<5)-hash)+char;
        hash |= 0; // Convert to 32bit integer
    }
    return hash;
};