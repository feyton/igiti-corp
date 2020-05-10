$(document).ready(function () {

    $("#id_image1").change(function () {
        var filePath = $(this)[0].files[0].name;
        $("#image1_label").text(filePath);
        $('#image1_clear_div').hide();
    });
    $("#id_image2").change(function () {
        var filePath = $(this)[0].files[0].name;
        $("#image2_label").text(filePath);
        $('#image2_clear_div').hide();
    });

    $(function () {
        $('.selectpicker').selectpicker();
    });


    $("#image1-clear_id").change(function () {
        if (this.checked) {
            $('#image1_input').hide()
        } else {
            $('#image1_input').show()
        }
    });
    $("#image2-clear_id").change(function () {
        if (this.checked) {
            $('#image2_input').hide()
        } else {
            $('#image2_input').show()
        }
    });

    // AJAX AND GRAPHS
    var endpoint = $("#allProducts").attr("data-url");
    var default_data = [];
    var labels = []
    $.ajax({
        method: 'GET',
        url: endpoint,
        success: function (all_data) {
            labels = all_data.labels
            default_data = all_data.default_data
            setProductChart();
            console.log(all_data);
            setIndexBigChart();
        },
        error: function (error_data) {
            console.log(error_data)
        }
    })

    function setProductChart() {
        var ctx = document.getElementById('allProducts').getContext('2d');
        gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
        gradientStroke.addColorStop(0, '#80b6f4');
        gradientStroke.addColorStop(1, chartColor);

        gradientFill = ctx.createLinearGradient(0, 170, 0, 50);
        gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
        gradientFill.addColorStop(1, "rgba(249, 99, 59, 0.40)");


        myChart = new Chart(ctx, {
            type: 'line',
            responsive: true,
            data: {
                labels: labels,
                datasets: [{
                    label: "Active Users",
                    borderColor: "#f96332",
                    pointBorderColor: "#FFF",
                    pointBackgroundColor: "#f96332",
                    pointBorderWidth: 2,
                    pointHoverRadius: 4,
                    pointHoverBorderWidth: 1,
                    pointRadius: 4,
                    fill: true,
                    backgroundColor: gradientFill,
                    borderWidth: 2,
                    data: default_data
                }]
            },
            options: gradientChartOptionsConfiguration
        });

    }
    function setIndexBigChart() {
        var ctx = document.getElementById('bigChartIndex').getContext("2d");

        var gradientStroke = ctx.createLinearGradient(500, 0, 100, 0);
        gradientStroke.addColorStop(0, '#80b6f4');
        gradientStroke.addColorStop(1, chartColor);

        var gradientFill = ctx.createLinearGradient(0, 200, 0, 50);
        gradientFill.addColorStop(0, "rgba(128, 182, 244, 0)");
        gradientFill.addColorStop(1, "rgba(255, 255, 255, 0.24)");

        var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
                datasets: [{
                    label: "Data",
                    borderColor: chartColor,
                    pointBorderColor: chartColor,
                    pointBackgroundColor: "#1e3d60",
                    pointHoverBackgroundColor: "#1e3d60",
                    pointHoverBorderColor: chartColor,
                    pointBorderWidth: 1,
                    pointHoverRadius: 7,
                    pointHoverBorderWidth: 2,
                    pointRadius: 5,
                    fill: true,
                    backgroundColor: gradientFill,
                    borderWidth: 2,
                    data: [50, 150, 100, 190, 130, 90, 150, 160, 120, 140, 190, 95]
                }]
            },
            options: {
                layout: {
                    padding: {
                        left: 20,
                        right: 20,
                        top: 0,
                        bottom: 0
                    }
                },
                maintainAspectRatio: false,
                tooltips: {
                    backgroundColor: '#fff',
                    titleFontColor: '#333',
                    bodyFontColor: '#666',
                    bodySpacing: 4,
                    xPadding: 12,
                    mode: "nearest",
                    intersect: 0,
                    position: "nearest"
                },
                legend: {
                    position: "bottom",
                    fillStyle: "#FFF",
                    display: false
                },
                scales: {
                    yAxes: [{
                        ticks: {
                            fontColor: "rgba(255,255,255,0.4)",
                            fontStyle: "bold",
                            beginAtZero: true,
                            maxTicksLimit: 5,
                            padding: 10
                        },
                        gridLines: {
                            drawTicks: true,
                            drawBorder: false,
                            display: true,
                            color: "rgba(255,255,255,0.1)",
                            zeroLineColor: "transparent"
                        }

                    }],
                    xAxes: [{
                        gridLines: {
                            zeroLineColor: "transparent",
                            display: false,

                        },
                        ticks: {
                            padding: 10,
                            fontColor: "rgba(255,255,255,0.4)",
                            fontStyle: "bold"
                        }
                    }]
                }
            }
        });
    }





})