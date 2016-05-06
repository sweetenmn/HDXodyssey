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
});