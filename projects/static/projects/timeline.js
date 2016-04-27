var completes = document.querySelectorAll(".complete");
;


function toggleComplete(){
  var lastComplete = completes[completes.length - 1];
  lastComplete.classList.toggle('complete');
}

