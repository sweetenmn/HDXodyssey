$(document).ready(function(){
    
    /*$("#progress_table .clickable").dblclick(function(){
        location.href = "student/project-status/" + $(this).attr("id");
    });

    $("#complete_table .clickable").dblclick(function(){
        location.href = "student/project-status/" + $(this).attr("id");
    });

    $("#awaiting_table .clickableP").dblclick(function(){
        location.href = "student/edit-form/" + $(this).attr("id");
    });
    $("#awaiting_table .clickableC").dblclick(function(){
        location.href = "student/edit-completion-form/" + $(this).attr("id");
    });*/
    $('#awaiting_table').DataTable( {
      select: 'single',
        language: {
            select: {
                rows: {
                    _: ''
                }
            }
        }
    } );
    $('#complete_table').DataTable( {
        select: 'single',
        language: {
            select: {
                rows: {
                    _: ''
                }
            }
        }                             
    } );
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
});