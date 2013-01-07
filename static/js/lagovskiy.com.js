function msg_info(title, message)
{
    $.notifier.broadcast(
        {
            ttl:title,
            msg:message,
            skin:'rounded',
            duration:5000
        });
}

function msg_error(title, message)
{
    $.notifier.broadcast(
        {
            ttl:title,
            msg:message,
            skin:'rounded.red',
            duration:5000
        });
}
