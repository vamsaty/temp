
function resetSetting(){

    var selec = document.getElementById("type_selection");
    selec.value = selec.children[0].value;

}

function enableUpload(candidate){
    var uploader = document.getElementById("uploadLabel");

    var selec = document.getElementById("type_selection");

    if(selec.value != selec.children[0].value){
        uploader.style.transition = "2s";
        uploader.style.display = "block";
    }else{
        uploader.style.display = "none";
    }
    

    var candId = -1;
    var len = candidate.childElementCount;
    var gal = document.getElementById("gallery");
    
    for(var i=0;i<len;i++){
        if(selec.value == selec.children[i].value){
            candId = i;
            if(i > 0)
                gal.children[i-1].style.display = "inline-flex";
        }else if(i > 0){
            gal.children[i-1].style.display = "none";
        }
    }


}

function incLike(insider){
    var likeCounts = insider.children[2].innerHTML;
    likeCounts = eval(likeCounts)+1;
    insider.children[2].innerHTML = likeCounts;
}


function killThis(victim){
    var x = victim.parentNode.parentNode.parentNode;
    x.remove();
}

