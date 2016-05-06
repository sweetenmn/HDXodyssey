$(document).ready(function(){

  $(".inputhr + label").addClass('btn btn-default btn-sm');
    $(".inputdesc + label").addClass('btn btn-default btn-sm');

    $('input[type="file"]').change(function(e){
        var fileName = e.target.files[0].name;
        if ($(this).attr('id') == 'narfile'){
            $("#narlabel").text(" " + fileName);
        } else if ($(this).attr('id') == 'hrfile'){
            $("#hrlabel").text(" " + fileName);
        } else if ($(this).attr('id') == 'descfile'){
            $("#desclabel").text(" " + fileName);
        }
    });

    CKEDITOR.replace('description')
    $('description').change(function(event) {
        handleFileSelect(event, 'description')
    });

    function handleFileSelect(event, editorName){
        readFileInputAsArrBuffer(event, function(arrayBuffer){
            mammoth.convertToHtml({arrayBuffer: arrayBuffer})
                .then(function(result) {
                    setTextEditor(result, editorName)
                })
                .done();
        });
    }
    function setTextEditor(result, editorName) {
        CKEDITOR.instances[editorName].setData(result.value);
    }
    function readFileInputAsArrBuffer(event, callback) {
        var file = document.getElementById('hrfile').files[0];
        var reader = new FileReader();
        reader.onload = function(e) {
            var arrayBuffer = e.target.result;
            callback(arrayBuffer);
        }
        reader.readAsArrayBuffer(file);
    }

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
});