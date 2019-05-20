<script >


    <!--angular.module('myApp', [])-->
    <!--.controller('HomeCtrl', function($scope, $http, $interval)-->
    <!--{-->
        <!--$scope.info = {};-->
        <!--$scope.CompanyName = "Stock Stalker";-->
        <!--$scope.documentTitle = ":-: StockStalker.com :-:";-->
         <!--$scope.stockName = "Security Name";-->
        <!--$scope.currentP = "Loading....";-->
        <!--$scope.openP = "Loading....";-->
        <!--$scope.highP = "Loading....";-->
        <!--$scope.lowP = "Loading....";-->
        <!--$scope.closeP = "Loading....";-->
        <!--$scope.datetime = "";-->

        <!--$scope.StocksArray = [];-->



        $scope.getChosenStockValues = function()
        {
				{
							 $http({
						method: 'POST',
						url: '/getChosenStockValues',
						data: {
							message: 'plss'
						}
					}).then(function(response) {
                                console.log("getChosenStockValues : " , response.data);
								//console.log('Login Response qwerty : ', response.data);
								$scope.currentP = response.data.currentP;
								$scope.stockName = response.data.title;
								$scope.documentTitle = response.data.title + " :-: StockStalker.com :-:";

					}, function(error) {
						console.log(error);
					});
				}

        }

        $scope.updateOCHLV = function()
        {
            console.log("In my own OCHLV")
				{
							 $http({
						method: 'POST',
						url: '/updateOCHLV',
						data: {
							message: 'Update Me About Open High Low Close Volume'
						}
					}).then(function(response) {
                                console.log("OCHL : " , response.data);
								$scope.openP = response.data.openP;
								$scope.closeP = response.data.closeP;
								$scope.highP = response.data.highP;
								$scope.lowP = response.data.lowP;
								$scope.volume = response.data.volume;

					}, function(error) {
						console.log(error);
					});
				}

        }

        $scope.getChartRecords = function()
        {

                $http(
                {
                    method: 'POST',
                    url: '/getChartRecords',
                    data:{ 'symbol': 'APPL'
                    }
                }).then(function(response)
                {
                     console.log('In scope.getChartRecords()', response.data);
                     $scope.chartrecords = response.data.chartrecords;
                     $scope.predictedValues = response.data.predictedValues;
                     console.log("Predicted Response", response.data.predictedValues);
                     var arr = [];
                     arr = $scope.chartrecords.split('\n');
                     var arr2 = [];
                     var finalArray = []
                     for(var i=0;i<arr.length;i++)
                     {
                        var arr2 = arr[i].split('|')
                        if(arr2.length > 5)
                        {
                            finalArray.push(arr2);
                        }
                     }

                     //console.log("Final Array  :", finalArray);

                     var pre_arr = [];
                     pre_arr = $scope.predictedValues.split('\n');
                     console.log("pre_arr : ", pre_arr);
                     var pre_arr2 = [];
                     var pre_finalArray = []
                     for(var i=0;i<pre_arr.length;i++)
                     {
                        if(pre_arr[i] == "")
                        {
                            continue;
                        }
                        var pre_arr2 = pre_arr[i].split('|')
                        pre_finalArray.push(pre_arr2);
                     }
                        console.log("pre_finalarray length  : ", pre_finalArray.length);
                     /*************************************/

                        for(var i=0;i<finalArray.length;i++)
                        {

                         var arr2 = [];
                         arr2.push(finalArray[i][0]);

                         arr2.push(parseFloat(finalArray[i][1]));
                         arr2.push(parseFloat(finalArray[i][3]));
                         arr2.push(parseFloat(finalArray[i][4]));
                         arr2.push(parseFloat(finalArray[i][2]));

                         arr2.push(finalArray[i][5]);
                          $scope.StocksArray.push(arr2);
                        }

                          console.log('StocksArray : ', $scope.StocksArray);
                          var len = $scope.StocksArray.length;
                          console.log('StocksArray length : ', len);


                          $scope.openP = finalArray[0][1];
						    $scope.closeP = finalArray[0][2];
							$scope.highP = finalArray[0][3];
							$scope.lowP = finalArray[0][4];
							$scope.volume = finalArray[0][5];

							$scope.currentP =finalArray[0][2];

                            var green = "#32ea32";
                            var red = "#fe3232";
                            var obj = {};

                            $scope.finalArray2 = []
							for(var i=0;i<finalArray.length;i++)
                            {
                                var localArray = [];
                                localArray.push(parseFloat(finalArray[i][1]));
                                localArray.push(parseFloat(finalArray[i][3]));
                                localArray.push(parseFloat(finalArray[i][4]));
                                localArray.push(parseFloat(finalArray[i][2]));
                                //localArray.push(finalArray[i][5]);

                                if(parseFloat(finalArray[i][2]) > parseFloat(finalArray[i][1]))
                                {
                                   obj = {x: new Date(finalArray[i][0]), y:localArray, color:green};
                                }
                                else
                                {
                                    obj = {x: new Date(finalArray[i][0]), y:localArray, color:red};
                                }

                             $scope.finalArray2.push(obj);
                            }
                            console.log("Final : ", $scope.finalArray2 )


                        /************************/
                        $('#chartContainer').html("");

                       var data = [];

                      for (var i = 0; i < len; i++)
                      {
                        data.push($scope.StocksArray[i]);
                      }
                      //console.log("Data  :", data);
                      $scope.StocksArray = [];
                         /************************/
                CanvasJS.addColorSet("greenShades",
                [//colorSet Array
                "#00e600"
                ]);
	var chart = new CanvasJS.Chart("chartContainer",
	{
	        colorSet: "greenShades",
		title:{
			text: ""
		},
		zoomEnabled: true,
		axisY: {
			includeZero:false,
			title: "Prices",
			prefix: "$ ",
			interval:0.09,
			gridThickness: 1
		},
		axisX: {
			interval:1,
			intervalType: "minute",
			labelAngle: -45
		},
		data: [
		{
		    xValueFormatString:"DD MMM, YYYY - h:m ",
			type: "candlestick",
			risingColor: green,
			dataPoints: $scope.finalArray2
		}
		]
	});

                        /***********************/
        <!--finalArray = pre_finalArray;-->
        <!--var len  = finalArray.length;-->
        <!--$scope.finalArray3 = [];-->
        <!--finalArray[0][1] = parseFloat(finalArray[0][1]);-->
        <!--var min = finalArray[0][1];-->
        <!--var max = 0.0;-->
        <!--var obj = {};-->
        <!--if(finalArray[0][1] >= finalArray[1][1])-->
                              <!--{-->
                                 <!--obj = { x: new Date(finalArray[0][0]), y: parseFloat(finalArray[0][1]), indexLabel: "gain", markerType: "triangle",  markerColor: "#6B8E23", markerSize: 10};-->
                              <!--}-->
                              <!--else-->
                              <!--{-->
                                 <!--obj = { x: new Date(finalArray[0][0]), y: parseFloat(finalArray[0][1]), indexLabel: "loss", markerType: "cross", markerColor: "tomato" , markerSize: 10};-->
                              <!--}-->
                              <!--$scope.finalArray3.push(obj);-->


							<!--for(var i=1;i<finalArray.length;i++)-->
                            <!--{-->
                            <!--finalArray[i][1] = parseFloat(finalArray[i][1]);-->
                                <!--if(finalArray[i][1] > max)-->
                                <!--{-->
                                    <!--max = finalArray[i][1];-->
                                <!--}-->
                                <!--if(finalArray[i][1] < min)-->
                                <!--{-->
                                    <!--min = finalArray[i][1];-->
                                <!--}-->



                                <!--finalArray[i-1][1] = parseFloat(finalArray[i-1][1]);-->

                                <!--if(finalArray[i-1][1] < finalArray[i][1]){-->
                                 <!--obj = { x: new Date(finalArray[i][0]), y: parseFloat(finalArray[i][1]), indexLabel: "gain", markerType: "triangle",  markerColor: "#6B8E23", markerSize: 10};-->

                                <!--}-->

                                <!--else if(finalArray[i-1][1] > finalArray[i][1]){-->

                                 <!--obj = { x: new Date(finalArray[i][0]), y: parseFloat(finalArray[i][1]), indexLabel: "loss", markerType: "cross", markerColor: "tomato" , markerSize: 10};-->

                                <!--}-->
                                <!--else-->
                                <!--{-->
                                    <!--obj = { x: new Date(finalArray[i][0]), y: parseFloat(finalArray[i][1]), indexLabel: "", markerType: "rectangle",  markerColor: "blue", markerSize: 8};-->

                                <!--}-->
                                <!--$scope.finalArray3.push(obj);-->




                            <!--}-->

                            <!--console.log("Final3 : ", $scope.finalArray3 )-->
        <!--/*********************/-->

        <!--var chart1 = new CanvasJS.Chart("chartContainer1",-->
    <!--{-->
      <!--title:{-->
       <!--text: ""-->
     <!--},-->
      <!--theme: "theme2",-->
     <!--axisX: {-->
       <!--interval:1,-->
			<!--intervalType: "minute",-->
			<!--labelAngle: -45-->
      <!--},-->
      <!--axisY:{-->
        <!--title: "Predicted Price",-->
         <!--minimum: min-0.6,-->
        <!--maximum: max+0.6,-->
		<!--interval:0.3,-->
		<!--gridThickness: 0-->
      <!--},-->
     <!--data: [-->
     <!--{-->
     <!--xValueFormatString:"DD MMM, YYYY - h:m ",-->
      <!--type: "line",-->
       <!--legendText: "Time",-->
      <!--dataPoints: $scope.finalArray3-->
    <!--}-->
    <!--]-->
  <!--});-->

chart.render();
<!--chart1.render();-->

        /**********************/


                })

        }

        $scope.streamLive2 = function()
        {
                $scope.getChartRecords();
                $interval( function(){ $scope.getChartRecords();}, 1000);
        }
        $scope.streamLive2();

        });
</script>



