

var $userSample = document.querySelector("#sample");
var $sampleMetaData = document.querySelector("#sampleMetaData");
var PIE = document.getElementById('pie');
var BUBBLE = document.getElementById('bubbleChart');

var pieTrace = {};
var bubbleTrace = {};

//generateChartData("BB_940");

///otu Descriptions
var otu_Desc= [];
Plotly.d3.json("/otu", function (error, response){
    otu_Desc = response;
});

//Runs when the page is loaded for the first time.
RenderOnRefresh();

function RenderOnRefresh() {
    // Populate the samples dropdown
    var SampleNames_url = "/names";
    Plotly.d3.json(SampleNames_url, function (error, response) {
        
        console.log(response);
        var SampleNames = response;
        SampleNames.sort();
        SampleNames.reverse();
        for (var a = 0; a < SampleNames.length; a++) {
            var $Option = document.createElement("Option");
            $Option.innerText = SampleNames[a];
            $userSample.appendChild($Option);
        }
        SampleChoice = SampleNames[0]
        $Option.innerText = SampleChoice
    });
    // Sample Metada
    renderSampleMetaData("BB_940");
   
    //Intial plots
    var sample = "BB_940";
    // Sample Metada
    var dataURL = "/samples/";
    Plotly.d3.json(dataURL + sample, function (error, response) {
        if (error)
            return console.warn(error);
        //Pie Chart
        var valuesPie = response[sample].slice(0, 10);
        var labelsPie = response['otu_ids'].slice(0, 10);
        var labelsPie1 = labelsPie.map(function (x) { return otu_Desc[x]; });
        console.log("Here!");
        pieTrace = {values: valuesPie, labels: labelsPie1, type: 'pie' };
         pieData = [pieTrace];
    
         //pie Plot layout
         var pieLayout = {
            width: 800,
            height:500,
            showlegend: true,
            legend: {
              
              "orientation" : "h",
              
            }
          };
        console.log(pieData);
        Plotly.plot(PIE, pieData,pieLayout) 


        //BubbleChart
        var yval = response[sample];
        var xval = response['otu_ids'];
        bubbleTrace = {
            x: xval,
            y: yval,
            text: xval.map(function (x) { return otu_Desc[x]; }),
            mode: 'markers',
            
            marker: {
                opacity: 0.8,
                size: yval,
                color: xval,
                colorscale: "Earth"
            }
        };
     //console.log("Here 1 !");
     bubbleData = [bubbleTrace];
      //bubble Plot layout      
      var bubbleLayout = {
            
        showlegend: false,
        height: 600,
        width: 1200
      };
      console.log(bubbleData);
      Plotly.newPlot("bubbleChart", bubbleData, bubbleLayout);

        
    });
  
   
        
    
}


function renderSampleMetaData(sample) {
    var metaDataURL = "/metadata/";
    Plotly.d3.json(metaDataURL + sample, function (error, response) {
        if (error)
            return console.warn(error);
        var metaData = response[0];
        $sampleMetaData.innerHTML = "";
        var x = Object.keys(metaData);
        var y = Object.values(metaData);

        for (var a = 0; a < x.length; a++) {
            var $p = document.createElement("p");
            console.log(x[a] + " : " + y[a]);
            $p.innerText = x[a] + " : " + y[a];
            $sampleMetaData.appendChild($p);
        }
    });
}

 // Update the plot with new data


function updateCharts(sample) {
    var dataURL = "/samples/";
    Plotly.d3.json(dataURL + sample, function (error, response) {
        if (error)
            return console.warn(error);
        //Pie Chart
        var new_valuesPie = response[sample].slice(0, 10);
        var new_labelsPie = response['otu_ids'].slice(0, 10);
        var new_labelsPie1 = new_labelsPie.map(function (x) { return otu_Desc[x]; });
       // var newPieTrace = { values: valuesPie, labels: labelsPie1, type: 'pie' };
        Plotly.restyle(PIE, "values", [new_valuesPie]);
        Plotly.restyle(PIE, "labels", [new_labelsPie1]);
        

       // Plotly.restyle(PIE, piedata, piedata);
        //BubbleChart
        var new_yval = response[sample];
        var new_xval = response['otu_ids'];
        var newtext = new_xval.map(function (x) { return otu_Desc[x]; });

        Plotly.restyle(BUBBLE,'x',[new_xval]);
        Plotly.restyle(BUBBLE,'y',[new_yval]);
        Plotly.restyle(BUBBLE,'text', [newtext]);
        Plotly.restyle(BUBBLE,'marker.size',[new_yval]);
        Plotly.restyle(BUBBLE,'marker.color',[new_xval]);
    });
}

 // Get new data whenever the dropdown selection changes
 function optionChanged(newSample) {
    console.log(newSample);
    renderSampleMetaData(newSample);
    updateCharts(newSample);
    };

 
