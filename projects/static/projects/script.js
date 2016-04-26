var clicked = '';

$(document).ready(function(){
	
	$("#progress_table .clickable").dblclick(function(){
		location.href = "project-status/" + $(this).attr("id");
	});

    $("#completion_table .clickable").dblclick(function(){
        location.href = "project-status/" + $(this).attr("id");
    });

    $("#saved_forms_table .clickable").dblclick(function(){
        location.href = "edit-form/" + $(this).attr("id");
    })

	$("#require").click(function(){
		alert("These are the requirements...");
	});

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

