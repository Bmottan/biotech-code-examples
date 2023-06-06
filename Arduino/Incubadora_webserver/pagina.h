const char pagina[] = R"=====(<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Incubadora - Dashboard</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,400,0,0" />
    <!-- Adding a chart using Chart.js -->
    <script src='https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.5.0/Chart.min.js'></script>
    <style>
        *{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Roboto', sans-serif;
        }
        body{
            background-color: #dfdfdf;
        }
        header{
            width: 100%;
            background-color: black;
            display: flex;
            align-items: center;
            color: white;
            font-size: 26px;
            padding: 20px 60px 20px 60px;
            justify-content: center;
        }

        .title{
            font-weight: bold;
        }

        .container{
            display: flex;
            justify-content: center;
            padding: 10px;
            font-size: 20px;
            flex-wrap: wrap;
        }

        section{
            width: 40%;
            margin: 10px;
            padding: 10px;
            background-color: white;
            border-radius: 20px;
            box-shadow: 5px 5px #f0f0f0;
            display: flex;
            flex-direction: column;
        }
        section_graph{
            
            margin: 10px;
            padding: 10px;
            background-color: white;
            border-radius: 20px;
            box-shadow: 5px 5px #f0f0f0;
            display: flex;
            flex-direction: column;
        }

        .item-head{
            display: flex;
            align-items: center;
        }

        .reading{
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        footer {
            background-color: black;
            padding: 1rem;
            color: #fff;
            position: relative;
            bottom: 0;
            width: 100%;
        }
    </style>
</head>
<body onload="javascript:init()">
    <header>
        <div class="logo"><i class="material-symbols-outlined">device_thermostat</i></div>
        <div class="title">&nbsp;&nbsp;   INCUBADORA &nbsp;&nbsp; </div>
        <div class="logo"><i class="material-symbols-outlined">water_drop</i></div>
    </header>
    
    <div class="container">
    
)=====";

    const char dia[] = R"=====(
        <section>
            <div class="item-head">
                <div class="logo"><i class="material-symbols-outlined">calendar_month</i></div>
                <div class="title">&nbsp;Data:</div>
            </div>
            <div class="reading">
                <div class="leitura">

)=====";

    const char hora[] = R"=====(</div>
            </div>
        </section>
        <section>
            <div class="item-head">
                <div class="logo"><i class="material-symbols-outlined">schedule</i></div>
                <div class="title">&nbsp;Hora:</div>
            </div>
            <div class="reading">
                <div class="leitura">
                        
)=====";

    const char tempera[] = R"=====(</div>
            </div>
        </section>
        <section>
            <div class="item-head">
                <div class="logo"><i class="material-symbols-outlined">device_thermostat</i></div>
                <div class="title">&nbsp;Temperatura:</div>
            </div>
            <div class="reading">
                <div class="leitura">
                      
)=====";

    const char umida[] = R"=====(</div>
                <div class="unidade">°C</div>
            </div>
        </section>  
        <section>
            <div class="item-head">
                <div class="logo"><i class="material-symbols-outlined">water_drop</i></div>
                <div class="title">&nbsp;Umidade:</div>
            </div>
            <div class="reading">
                <div class="leitura">
    
)=====";

    const char grafi[] = R"=====(</div>
                <div class="unidade">%</div>
            </div>
        </section>
        <section_graph>
            <div class="item-head">
                <div class="logo"><i class="material-symbols-outlined">query_stats</i></div>
                <div class="title">&nbsp;Gráfico:</div>
            </div>
            <div class="reading">
                <div>
                  <canvas id="line-chart" width="400" height="200"></canvas>
                </div>
            </div>
        </section_graph>

    </div>

)=====";

    const char rodape[] = R"=====(</div>
  <!-- Adding a websocket to the client (webpage) -->
  <script>
    var webSocket, dataPlot;
    var maxDataPoints = 200;
    function removeData(){
      dataPlot.data.labels.shift();
      dataPlot.data.datasets[0].data.shift();
    }
    function addData(label,data){
      if(dataPlot.data.labels.length > maxDataPoints) removeData();
      dataPlot.data.labels.push(label);
      dataPlot.data.datasets[0].data.push(data);
      dataPlot.update();
    }
    function init(){
      webSocket = new WebSocket('ws://' + window.location.hostname + ':81/');
      dataPlot = new Chart(document.getElementById("line-chart"), {
        type: 'line',
        data: {
          labels: [],
          datasets: [{
            data: [],
            label: "Temperatura",
            borderColor: "#3e95cd",
            fill: false
          }]
        }
 
      
      });
      webSocket.onmessage = function(event){
        var data = JSON.parse(event.data);
        var today = new Date();
        var t = today.getHours()+":"+ today.getMinutes()+":"+today.getSeconds();
        addData(t, data.value);
      }
    }
   </script>
      <footer>
          <div class="title">Desenvolvido por: BMN</div>
      </footer>
</body>
</html>)=====";
