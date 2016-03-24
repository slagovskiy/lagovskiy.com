// TAG
//url_tag_get_all = '{% url 'admin_tag_get' 0 %}';
//url_tag_get = '{% url 'admin_tag' %}';
//url_tag_save = '{% url 'admin_tag_save' %}';

function loadTagData()
{
    $('#dataContainer').html('<div class="loader"></div>');
    $.ajax({
        url : url_tag_get_all,
        cashe: false
    }).done(function(data){
        var jdata = jQuery.parseJSON(data);
        var template = $.templates('#dataTagTemplate');
        $('#dataTagContainer').html(template.render(jdata));
    });
}

function editTagData(key)
{
    $.ajax({
        url :url_tag_get + key + '/',
        cashe: false
    }).done(function(data){
        var jdata = jQuery.parseJSON(data);
        var template = $.templates('#dataTagEdit');
        $('#dataTagForm').html(template.render(jdata));
    });

    $('.open-data-form').fancybox({
        padding: 0,
        type: 'inline',
        title: '',
        modal: false,
        autoSize: true
    });
}

function deleteTagItem() {
    $("#dataTagForm form #deleted").val('true');
    saveTagData();
}

function restoreTagItem() {
    $("#dataTagForm form #deleted").val('false');
    saveTagData();
}

function saveTagData() {
    $.ajax({
            type: 'POST',
            url: url_tag_save,
            data: $("#dataTagForm form").serialize()
        })
        .done(function(data){
            if(data=='ok') {
                notice('green', 'saved');
                $.fancybox.close();
                loadTagData();
            }
            else {
                notice('red', data);
            }
        })
        .fail(function(){
            notice('red', 'data transfer error');
        });
    $("#dataTagForm form").submit(function(){
        return false;
    });
}

//CATEGORY
//url_category_get_all = '{% url 'admin_category_get' 0 %}';
//url_category_get = '{% url 'admin_category' %}';
//url_category_save = '{% url 'admin_category_save' %}';


function loadCategoryData()
{
    $('#dataCategoryContainer').html('<div class="loader"></div>');
    $.ajax({
        url : url_category_get_all,
        cashe: false
    }).done(function(data){
        var jdata = jQuery.parseJSON(data);
        var template = $.templates('#dataCategoryTemplate');
        $('#dataCategoryContainer').html(template.render(jdata));
    });

}

function editCategoryData(key)
{
    $.ajax({
        url : url_category_get + key + '/',
        cashe: false
    }).done(function(data){
        var jdata = jQuery.parseJSON(data);
        var template = $.templates('#dataCategoryEdit');
        $('#dataCategoryForm').html(template.render(jdata));
    });

    $('.open-data-form').fancybox({
        padding: 0,
        type: 'inline',
        title: '',
        modal: false,
        autoSize: true
    });
}

function deleteCategoryItem() {
    $("#dataCategoryForm form #deleted").val('true');
    saveCategoryData();
}

function restoreCategoryItem() {
    $("#dataCategoryForm form #deleted").val('false');
    saveCategoryData();
}

function saveCategoryData() {
    $.ajax({
                type: 'POST',
                url:  url_category_save,
                data: $("#dataCategoryForm form").serialize()
            })
            .done(function(data){
                if(data=='ok') {
                    notice('green', 'saved');
                    $.fancybox.close();
                    loadCategoryData();
                }
                else {
                    notice('red', data);
                }
            })
            .fail(function(){
                notice('red', 'data transfer error');
            });
    $("#dataCategoryForm form").submit(function(){
        return false;
    });
}

$(document).ready(function() {
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
