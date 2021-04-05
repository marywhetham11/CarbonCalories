function createLine(data, targetDiv) {
    am4core.useTheme(am4themes_animated);

    // Create chart instance
    var chart = am4core.create(targetDiv, am4charts.XYChart);
    chart.paddingRight = 20;

    for (let i = 0; i < data.length; i++) {
        var dateSub = (data[i].date).toString().substring(5, 16);
        data[i].date = new Date(dateSub);
    }

    // Add data
    chart.data = data;

    // Create axes
    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.minGridDistance = 50;
    dateAxis.renderer.grid.template.location = 0.5;
    dateAxis.startLocation = 0.5;
    dateAxis.endLocation = 0.5;
    dateAxis.title.text = "Date";

    // Create value axis
    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.title.text = "Carbon Score";

    // Create series
    var series = chart.series.push(new am4charts.LineSeries());
    series.dataFields.valueY = "value";
    series.dataFields.dateX = "date";
    series.strokeWidth = 3;

    chart.cursor = new am4charts.XYCursor();
    chart.cursor.snapToSeries = series;
    chart.cursor.xAxis = dateAxis;
}