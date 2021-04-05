function createPie(data, targetDiv) {
    // Create chart instance
    var chart = am4core.create(targetDiv, am4charts.PieChart);
    chart.innerRadius = am4core.percent(35);
    chart.radius = am4core.percent(60);

    // Add data
    chart.data = data;

    // Add and configure Series
    var pieSeries = chart.series.push(new am4charts.PieSeries());
    pieSeries.dataFields.value = "quantity";
    pieSeries.dataFields.category = "type";

    pieSeries.slices.template.propertyFields.fill = "color";
    pieSeries.slices.template.fillOpacity = 1;

    pieSeries.labels.template.maxWidth = 110;
    pieSeries.labels.template.wrap = true;
    pieSeries.labels.template.text = "{category}";
}