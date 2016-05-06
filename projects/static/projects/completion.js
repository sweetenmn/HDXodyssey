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
    $("#CompRequire").click(function(e){
        e.preventDefault();
        alert("Limit yourself to 150 words and a single paragraph - multiple paragraphs will be combined into one for the transcript. Write in complete sentences, preferably using first person. Briefly describe the basic details of your project: who, what, when, where. The first time you name a company, an organization, a position, or a program, use the full title with the abbreviation in parentheses. After that you can refer to it by the abbreviation. Include one or two sentences about the value of the experience. Try to pinpoint some specific learning outcomes or benefits to your personal growth, such as insights gained or skills improved. Avoid grand generalizations or hyperbolic statements.");
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
