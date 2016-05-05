var clicked = '';
var groupNo = 0;
var added = false;

$(document).ready(function(){
    
    $("#progress_table .clickable").dblclick(function(){
        location.href = "project-status/" + $(this).attr("id");
    });

    $("#completion_table .clickable").dblclick(function(){
        location.href = "project-status/" + $(this).attr("id");
    });

    $("#saved_forms_table .clickable").dblclick(function(){
        location.href = "edit-form/" + $(this).attr("id");
    });

	$("#CompRequire").click(function(){
		alert("Limit yourself to 150 words and a single paragraph - multiple paragraphs will be combined into one for the transcript. Write in complete sentences, preferably using first person. Briefly describe the basic details of your project: who, what, when, where. The first time you name a company, an organization, a position, or a program, use the full title with the abbreviation in parentheses. After that you can refer to it by the abbreviation. Include one or two sentences about the value of the experience. Try to pinpoint some specific learning outcomes or benefits to your personal growth (e.g. My communication skills improved. I gained insight into the many facets of running a small business.). Avoid grand generalizations or hyperbolic statements.");
    });

    // $("#require").click(function(){
    //     alert("These are the requirements...");
    // });

    $(".inputnar + label").addClass('btn btn-default btn-sm');
    $(".inputhr + label").addClass('btn btn-default btn-sm');
    $(".inputdesc + label").addClass('btn btn-default btn-sm');

    $('#progress_table').DataTable( {
    	select: 'single',
        language: {
            select: {
                rows: {
                    _: ''
                }
            }
        }

    } );
                  
    $('#completion_table').DataTable( {
        select: 'single',
        language: {
            select: {
                rows: {
                    _: ''
                }
            }
        }        
                                   
    } );
    $('#saved_forms_table').DataTable( {
        select: 'single',
        language: {
            select: {
                rows: {
                    _: ''
                }
            }
        }                                                   
    } );

    $("#party").change(function() {
        if ($(this).val() == "Group" && groupNo==0){
            var label = "group-" + groupNo;
            $('#groupdiv').append("<br><div id="+
                label+"><input type='text' size=35 name='"+label+
                "'' placeholder='Email for additional member #"+(groupNo+1)+"'></div> ");
            $('#addmember').addClass('btn btn-default btn-sm');
            $('#addmember').text("+");
            $('#remmember').addClass('btn btn-default btn-sm');
            $('#remmember').text("-");
            groupNo++;
        } else if ($(this).val() == "Individual"){
            removeGroup();
        }
    });

    $("#addmember").click(function() {
        var label = "group-" + groupNo;
        $('#groupdiv').append("<div id="+
            label+"><input type='text' size=35 name='"+label+
            "'' placeholder='Email for additional member #"+(groupNo+1)+"'></div> ");
        groupNo++;
    });
    $("#remmember").click(function() {
        if (groupNo > 1){
            $('#group-'+(groupNo-1)).remove();
            groupNo--;
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
    }






	$(":submit").click(function() { 
		clicked = this.value 
	});
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

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */
                 
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

