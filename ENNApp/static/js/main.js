$(document).ready(function(){
    $( "#submitUploadDataset" ).click(function() {
        
        const file = $("#dataSet").val();
        
        if(file == ""){
            showError("No file selected.", "Error!");
        }else{
            if(file.split(".").pop() != "csv"){
                showError("The file extension must be .csv", "Error!");
            }else{
                $("#uploadDataset").submit();
            }
        }
    });
});


function showError(mensaje, boldMensage=""){
    $("#errorText").text(mensaje);
    $("#errorBoldText").text(boldMensage);
    $("#msjErr").show();
}

function hideError(){
    $("#msjErr").hide();
}
