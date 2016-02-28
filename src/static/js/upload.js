var UPLOAD_URL = "/upload";

var PENDING_FILES  = [];


function initUpload() {
    initDropbox();
    $("#filePicker").on("change", function() {
        handleFiles(this.files);
        $("#filePicker").next().text('Selected ' + this.files.length + ' file(s).');
    });
    $("#upload-button").on("click", function(e) {
        e.preventDefault();
        doUpload();
    });
    $("#progress").hide();
}


function doUpload() {
    var $progressBar = $(".progressBar");
    $("#upload-form :input").attr("disabled", "disabled");
    $progressBar.css({"width": "0%"});
    $("#progress").show();
    fd = collectFormData();

    for (var i = 0, ie = PENDING_FILES.length; i < ie; i++) {
        fd.append("file", PENDING_FILES[i]);
    }

    fd.append("__ajax", "true");

    var xhr = $.ajax({
        xhr: function () {
            var xhrobj = $.ajaxSettings.xhr();
            if (xhrobj.upload) {
                xhrobj.upload.addEventListener("progress", function (event) {
                    var percent = Math.ceil((event.loaded * 100) / event.total);
                    $progressBar.css({"width": percent + "%"});
                    $progressBar.text(percent + "%");
                }, false)
            }
            return xhrobj;
        },
        url: UPLOAD_URL,
        method: "POST",
        contentType: false,
        processData: false,
        cache: false,
        data: fd
    })
    .done(function(data) {
        if (data=="ok") {
            notice("green", "uploaded");
        } else {
            notice("red", data);
        }
        $progressBar.css({"width": "100%"});
        $("#progress").hide();
        $("#upload-form :input").removeAttr("disabled");
        loadFolderData($('#folder_key').val());
    })
    .fail(function() {
        notice("red", "error send file");
        $("#progress").hide();
        $("#upload-form :input").removeAttr("disabled");
    });
}

function resetForm(e) {
    e.wrap('<form>').closest('form').get(0).reset();
    e.unwrap();
    $('#filePicker').next().text('Choose a file');
}


function collectFormData() {
    var fd = new FormData();

    $("#upload-form :input").each(function() {
        var $this = $(this);
        var name  = $this.attr("name");
        var type  = $this.attr("type") || "";
        var value = $this.val();

        if (name === undefined) {
            return;
        }

        if (type === "file") {
            return;
        }

        if (type === "checkbox" || type === "radio") {
            if (!$this.is(":checked")) {
                return;
            }
        }

        fd.append(name, value);
    });

    return fd;
}


function handleFiles(files) {
    for (var i = 0, ie = files.length; i < ie; i++) {
        PENDING_FILES.push(files[i]);
    }
}


function initDropbox() {
    var $dropbox = $(".dropbox");

    $dropbox.on("dragenter", function(e) {
        e.stopPropagation();
        e.preventDefault();
        $(this).addClass("active");
    });

    $dropbox.on("dragover", function(e) {
        e.stopPropagation();
        e.preventDefault();
    });

    $dropbox.on("drop", function(e) {
        e.preventDefault();
        $(this).removeClass("active");

        var files = e.originalEvent.dataTransfer.files;
        handleFiles(files);

        $dropbox.text(PENDING_FILES.length + " files ready for upload!");
    });

    function stopDefault(e) {
        e.stopPropagation();
        e.preventDefault();
    }
    $(document).on("dragenter", stopDefault);
    $(document).on("dragover", stopDefault);
    $(document).on("drop", stopDefault);
}
