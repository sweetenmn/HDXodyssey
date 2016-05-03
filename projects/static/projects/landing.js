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
)