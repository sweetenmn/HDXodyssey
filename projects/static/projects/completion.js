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

});