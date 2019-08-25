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

/*
var url = new URL("http://foo.bar/?x=1&y=2");

// If your expected result is "http://foo.bar/?x=1&y=2&x=42"
url.searchParams.append('x', 42);

// If your expected result is "http://foo.bar/?x=42&y=2"
url.searchParams.set('x', 42);
*/

function showError(menssage, boldMensage=""){
    hideError();
    hideCorrectMessage();
    $("#errorText").text(menssage);
    $("#errorBoldText").text(boldMensage);
    $("#msjErr").show();
}

function hideError(){
    $("#msjErr").hide();
}

function showCorrectMessage(menssage, boldMensage=""){
    hideError();
    hideCorrectMessage();
    $("#correctText").text(menssage);
    $("#correctBoldText").text(boldMensage);
    $("#msjCorrect").show();
}

function hideCorrectMessage(){
    $("#msjCorrect").hide();
}


$(document).ready(function(){
  $( "#regiterButtom" ).click(function() {

      var emailRegExp = new RegExp(/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/);
      if($("#inputPassword").val() != $("#inputConfirmPassword").val() 
          || $("#inputPassword").val() == ""
          || !emailRegExp.test(String($("#inputEmail").val()).toLowerCase())){
        $("#registerError").show();
      }else{
        $("#registerForm").submit();
      }
      

  });
});


//Delete modal
$(document).on("click", ".deletebuttom", function () {
  var myBookId = $(this).data('url');
  $("#deleteButonModal").click(function() {
    location.href=myBookId;
  });
});

// Call the dataTables jQuery plugin
$(document).ready(function() {
  if(isAdmin){
    $('.dataSetTable').DataTable({
      "columns": [
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": false }
      ]
    });
  }else{
    $('.dataSetTable').DataTable({
      "columns": [
        { "orderable": true },
        { "orderable": true },
        { "orderable": true },
        { "orderable": false }
      ]
    });
  } 
});

$(document).ready(function() {
  $('#dataframeSample').addClass("table table-bordered");
  $('#dataframeSample').attr("width","100%");
  $('#dataframeSample').attr("cellspacing","0");
  $('#dataframeSample').DataTable();
});

$(document).ready(function() {
  $('#dataframeDescription').addClass("table table-bordered");
  $('#dataframeDescription').attr("width","100%");
  $('#dataframeDescription').attr("cellspacing","0");
  $('#dataframeDescription').DataTable({
    //"pageLength": 50
    "paging": false
  });
});

$(document).ready(function() {
  $('#dataframeInfo').addClass("table table-bordered");
  $('#dataframeInfo').attr("width","100%");
  $('#dataframeInfo').attr("cellspacing","0");
  $('#dataframeInfo').DataTable();
});


$(document).ready(function() {
  $('#correlations').addClass("table table-bordered");
  $('#correlations').attr("width","100%");
  $('#correlations').attr("cellspacing","0");
  $('#correlations').DataTable(
    { 
      "columnDefs": [ { "orderable": false, "targets": 0 } ],
      'rowCallback': function(row, data, index){
        for(var index in row.cells){
          var cellValue = row.cells[index].innerText;
          if(!isNaN(cellValue)){
            if(cellValue > 0){
              //Rojo relacionadas
              $(row.cells[index]).css('background-color', 'hsl(0, 100%, '+( Math.round(100 - (cellValue * 50 )) )+'%)');
              //$(row.cells[index]).css('color', 'hsl(0, 100%, '+( Math.round(95 - (cellValue * 45)) )+'%)');
            }else{
              //Azul inversamente relacionadas
              $(row.cells[index]).css('background-color', 'hsl(240, 100%, '+( Math.round(100 - (cellValue * -50)) )+'%)');
              //$(row.cells[index]).css('color', 'hsl(240, 100%, '+( Math.round(95 - (cellValue * -45)) )+'%)');
            }
          }
        }
      }
    }
  );
});
  
/*

//Plot
// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Area Chart Example
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ["Mar 1", "Mar 2", "Mar 3", "Mar 4", "Mar 5", "Mar 6", "Mar 7", "Mar 8", "Mar 9", "Mar 10", "Mar 11", "Mar 12", "Mar 13"],
    datasets: [{
      label: "Sessions",
      lineTension: 0.3,
      backgroundColor: "rgba(2,117,216,0.2)",
      borderColor: "rgba(2,117,216,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(2,117,216,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: [10000, 30162, 26263, 18394, 18287, 28682, 31274, 33259, 25849, 24159, 32651, 31984, 38451],
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 7
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: 40000,
          maxTicksLimit: 5
        },
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
    legend: {
      display: false
    }
  }
});
*/



//*Show DatasetView**/

$("#radioOverwriteFile").change(function() {
  $("#newFileName").prop("disabled", true);
  $("#newFileNameLabel").addClass("customDisable");
});

$("#radioNotOverwriteFile").change(function() {
  $("#newFileName").prop("disabled", false);
  $("#newFileNameLabel").removeClass("customDisable");
});


$("input[type=radio][name=valuesNull]").change(function() {
  if($("#valuesNullD").prop( "checked")){
    $("#customNumber").prop("disabled", false);
  }else{
    $("#customNumber").prop("disabled", true);
  }
});

$("input[type=checkbox][name='deleteCols[]']").change(function() {
  var colum = $(this).val();
  var oneHotCheckBox = $("#oneHot"+colum);
  if(!oneHotCheckBox.hasClass("categoric")){
    if($(this).prop( "checked")){
      oneHotCheckBox.prop("disabled", true);
      oneHotCheckBox.prop("checked", false);
    }else{
      oneHotCheckBox.prop("disabled", false);
    }
  }
  if($(this).prop( "checked")){
    $("#oneHotLabel"+colum).addClass("crossLine");
  }else{
    $("#oneHotLabel"+colum).removeClass("crossLine");
  }
});
