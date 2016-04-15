var clicked = '';

$(document).ready(function(){

    $('#progressTable').DataTable({
        select: true
    });

	$(":submit").click(function() { 
		clicked = this.value 
	});

	$('#post-project').on('submit', function(event){
		event.preventDefault();
		switch(clicked){
			case "ss":
				console.log("save and submit");
				console.log($('#title').val());
				console.log($('#party :selected').attr('id'));
				console.log($('#super :selected').attr('id'));
				submit_proposal();
				break;
			case "save":
				console.log("save");
				save_proposal();
				break;
			case "del":
				console.log("delete");
				delete_proposal();
				break;
			default:
				break;
		}
	});
    
    $('a.btn-ok, #dialog-overlay, #dialog-box').click(function () {
        $('#dialog-overlay, #dialog-box').hide();
        return false;
    });
                  
    // if user resize the window, call the same function again
    // to make sure the overlay fills the screen and dialogbox aligned to center
    $(window).resize(function () {
                                   
        //only do it if the dialog box is not hidden
        if (!$('#dialog-box').is(':hidden')) popup();
    });
                  
//    function() {
//        var dialog = document.getElementById('window');
//        document.getElementById('#show').onclick = function() {
//            dialog.show();
//        };
//        document.getElementById('#exit').onclick = function() {
//            dialog.close();
//        };
//    };
                  
	function submit_proposal(){
		$.ajax({
			url : "submit_proposal/",
			type : "POST",
			datatype: 'json',
			data : { title : $("#title").val(), super : $('#super :selected').attr('id').substring(3), category : $("#cat :selected").attr('id')},success : function(json) {
				console.log(json);
				console.log("success");
			},error : function(jqXHR, textStatus, errorThrown){
				console.log(textStatus, errorThrown);
			}

		});
	};

    // This function gets cookie with a given name
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


function popup(message) {
    
    // get the screen height and width
    var maskHeight = $(document).height();
    var maskWidth = $(window).width();
    
    // calculate the values for center alignment
    var dialogTop =  (maskHeight/3) - ($('#dialog-box').height());
    var dialogLeft = (maskWidth/2) - ($('#dialog-box').width()/2);
    
    // assign values to the overlay and dialog box
    $('#dialog-overlay').css({height:maskHeight, width:maskWidth}).show();
    $('#dialog-box').css({top:dialogTop, left:dialogLeft}).show();
    
    // display the message
    $('#dialog-message').html(message);
    
}
