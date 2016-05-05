var groupNo = 0;

$(document).ready(function(){
    // $("#require").click(function(){
    //     alert("GGGGGGGGGGGGGGGJALDAFL:KDS:LKGDSGKLJKLGSKJLKLGSJKL:G:GS:L:KLGJKL:GLFJG:FLKLKF: These are the requirements...");
    // });
    $(".inputnar + label").addClass('btn btn-default btn-sm');
    // CKEDITOR.replace('description')
    // $('description').change(function(event) {
    //     handleFileSelect(event, 'description')
    // });
    // Initializing the text editor
    CKEDITOR.replace('narrative')
    //Fire when a new file is uploaded
    $("#narfile").change(function(event) {
        //Convert to HTML
        handleFileSelect(event, 'narrative')
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
        var file = document.getElementById('narfile').files[0];
        var reader = new FileReader();
        reader.onload = function(e) {
            var arrayBuffer = e.target.result;
            callback(arrayBuffer);
        }
        reader.readAsArrayBuffer(file);
    }


    $("#party").change(function() {
        if ($(this).val() == "Group" && groupNo==0){
            groupNo++;
            var label = "group-" + groupNo;
            $('#groupsize').val(String(groupNo));
            $('#groupdiv').append("<br><div id="+
                label+"><input type='text' size=35 name='"+label+
                "'' placeholder='Email for additional member #"+(groupNo)+"'></div> ");
            $('#addmember').addClass('btn btn-default btn-sm');
            $('#addmember').text("+");
            $('#remmember').addClass('btn btn-default btn-sm');
            $('#remmember').text("-");
           
        } else if ($(this).val() == "Individual"){
            removeGroup();
        }
    });

    $("#addmember").click(function() {
        groupNo++;
        var label = "group-" + groupNo;
        $('#groupdiv').append("<div id="+
            label+"><input type='text' size=35 name='"+label+
            "'' placeholder='Email for additional member #"+(groupNo)+"'></div> ");
        $('#groupsize').val(String(groupNo));
    });
    $("#remmember").click(function() {
        if (groupNo > 1){
            $('#group-'+(groupNo)).remove();
            groupNo--;
            $('#groupsize').val(String(groupNo));
        } else {
            removeGroup();

        }
    });

    function removeGroup(){
        $('#groupdiv').empty()
        $("#party").val("Individual");
        $('#addmember').removeClass('btn btn-default btn-sm');
        $('#addmember').text("");
        $('#remmember').removeClass('btn btn-default btn-sm');
        $('#remmember').text("");
        groupNo=0;
        $('#groupsize').val(String(groupNo));
    };

    $(":submit").click(function() { 
        clicked = this.value 
    });

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
    