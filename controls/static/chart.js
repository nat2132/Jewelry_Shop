document.addEventListener("DOMContentLoaded", function() {
// ================ Chart ==================

// Bar Chart

var barChartOptions = {
    series: [{
    data: [10, 8, 6, 4, 2]
  }],
    chart: {
    type: 'bar',
    height: 350,
    toolbar: {
        show: false
    },
  },
  colors: [
    "#246dec",
    "#cc3c43",
    "#367952",
    "#f5b74f",
    "#4f35a1"
  ],
  plotOptions: {
    bar: {
      distributed: true,
      borderRadius: 4,
      horizontal: false,
      columnWidth: '40%',
    }
  },
  dataLabels: {
    enabled: false
  },
  legend:{
    show:false
  },
  xaxis: {
    categories: ["Tezeta Cuffs", "Rings", "Bracelets", "Earrings", "Anklets"
    ],
  },
  yaxis: {
    title: {
      text: 'Count'
    }
  }
  };

  var barChart = new ApexCharts(document.querySelector("#bar-chart"), barChartOptions);
  barChart.render();

// Area Chart
      
  var areaChartOptions = {
    series: [{
    name: 'Purchase Orders',
    type: 'area',
    data: [31, 40, 28, 51, 42, 109, 100]
  }, {
    name: 'Sales Orders',
    type: 'line',
    data: [11, 32, 45, 32, 34, 52, 34, 41]
  }],
    chart: {
    height: 350,
    type: 'area',
    toolbar: {
      show: false
    },
  },
  colors: ["#4f35a1", "#246dec"],
  dataLabels: {
    enabled: false
  },
  stroke: {
    curve: 'smooth'
  },
  fill: {
    type:'solid',
    opacity: [0.35, 1],
  },
  labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul"],
  markers: {
    size: 0
  },
  yaxis: [
    {
      title: {
        text: 'Purchase Orders',
      },
    },
    {
      opposite: true,
      title: {
        text: 'Sales Orders',
      },
    },
  ],
  tooltip: {
    shared: true,
    intersect: false,
  }
  };

  var areaChart = new ApexCharts(document.querySelector("#area-chart"), areaChartOptions);
  areaChart.render();

});