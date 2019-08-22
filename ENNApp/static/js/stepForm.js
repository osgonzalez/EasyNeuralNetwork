
    
var currentTab = 0; // Current tab is set to be the first tab (0)

function showTab(n) {
    // This function will display the specified tab of the form...
    var x = $(".tabStep");
    $(x[n]).show("slow");
    //... and fix the Previous/Next buttons:
    if (n == 0) {
    document.getElementById("prevBtn").style.display = "none";
    } else {
    document.getElementById("prevBtn").style.display = "inline";
    }
    if (n == (x.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
    $("#nextBtn").removeClass("btn-primary");
    $("#nextBtn").addClass("btn-success");
    } else {
        document.getElementById("nextBtn").innerHTML = "Next";
        $("#nextBtn").removeClass("btn-success");
        $("#nextBtn").addClass("btn-primary");
    }
    //... and run a function that will display the correct step indicator:
    fixStepIndicator(n)
}

function nextPrev(n) {
    // This function will figure out which tab to display
    var x = document.getElementsByClassName("tabStep");
    // Exit the function if any field in the current tab is invalid:
    if (n == 1 && !validateForm()) return false;
    // Hide the current tab:
    $($(".tabStep")).hide("slow");
    // Increase or decrease the current tab by 1:
    currentTab = currentTab + n;
    // if you have reached the end of the form...
    if (currentTab >= x.length) {
    // ... the form gets submitted:
    document.getElementById("regForm").submit();
    return false;
    }
    // Otherwise, display the correct tab:
    showTab(currentTab);
}

function validateForm() {
    return true;
}

function fixStepIndicator(n) {
    // This function removes the "active" class of all steps...
    var i, x = document.getElementsByClassName("step");
    for (i = 0; i < x.length; i++) {
    x[i].className = x[i].className.replace(" active", "");
    }
    //... and adds the "active" class on the current step:
    x[n].className += " active";
}

$(document).ready(function(){
    if($(".stepForm").length){
        showTab(currentTab);
    }
});