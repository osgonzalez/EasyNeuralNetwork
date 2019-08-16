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

      var emailRegExp = '/^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/';
      if($("#inputPassword").val() != $("#inputConfirmPassword").val() 
          || $("#inputPassword").val() == ""
          || !emailRegExp.test(String(email).toLowerCase())){
        $("#registerError").show();
      }else{
        $("#registerForm").submit();
      }
      

  });
});


// Call the dataTables jQuery plugin
$(document).ready(function() {
    $('#dataTable').DataTable();
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