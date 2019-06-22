function buildMetadata(sample) {
metaurl = "/metadata/"+sample
  // Build the metadata panel
  // Use `d3.json` to fetch the metadata for a sample
  d3.json(metaurl, function(data){

    // Use d3 to select the panel with id of `#sample-metadata`
    var table = d3.select('#sample-metadata');

    // clear the input value
    d3.select("#sample-metadata") = "";

    //loop through each key,value pair to display
      Object.entries(data).forEach(function([key, value]) {
        var row = table.append('tr');
        var cell = row.append ('td');
        cell.text(key + ':  ');
        cell = row.append ('td');
        cell.text('   ' + value);
        
      });
  });
}

function buildScatter(sample) {
  url = "/scattersamples/" + sample
   
  // @TODO: Use `d3.json` to fetch the sample data for the plots
  d3.json(url, function(response) {
    var otu_ids = response.otu_ids
    var sample_values = response.sample_values
    var otu_labels = response.otu_labels
    
    // @TODO: Build a Bubble Chart using the sample data
    var trace1 = {
      x: otu_ids,
      y: sample_values,
      name:"Bubble Chart",
      type: "scatter",
      mode: 'markers',
      text: otu_labels,
      marker:  {
        size: sample_values,
        color:  otu_ids
      }
    }
    var bubbledata = [trace1]
    var layout = {
      xaxis: {title: "otu ids"},
      yaxis: {title: "sample values"},
      title: "Belly Button"
    };
    Plotly.newPlot("bubble", bubbledata, layout);
  });
}
function buildPie(sample){
  pieurl = "/piesamples/" + sample
 
    // @TODO: Build a Pie Chart
        d3.json(pieurl, function(sorted) {
      var sorted_otu_ids = sorted.otu_ids
      var sorted_sample_values = sorted.sample_values
      var sorted_otu_labels = sorted.otu_labels
          
    var trace2 = {
      values: sorted_sample_values,
      labels: sorted_otu_ids,
      hovertemplate: sorted_otu_labels,
      hoverinfo: 'text',
      type: "pie"
    };
    var piedata = [trace2];
    var layout = {
        title: "Top 10 Bacterium for Sample",
        legend: {title: "Top 10 Bacteria for sample"}
      };
    Plotly.newPlot("pie", piedata, layout);
  });
}

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");
console.log("hello")
  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

    // Use the first sample from the list to build the initial plots
    const firstSample = sampleNames[0];
    console.log(firstSample)
    buildPie(firstSample);
    buildScatter(firstSample);
    buildMetadata(firstSample);
  });
}

function optionChanged(newSample) {
  console.log(newSample)
  // Fetch new data each time a new sample is selected
  buildScatter(newSample);
  buildPie(newSample);
  buildMetadata(newSample);
}

// Initialize the dashboard
init();
