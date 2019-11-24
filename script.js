function showGraph(){
  ajaxGetRequest('/pie', showPie);
	ajaxGetRequest('/table', showTable);
}

function ajaxGetRequest(path, callback) {
    let request = new XMLHttpRequest();
    request.onreadystatechange = function() {
  	  if (this.readyState===4 && this.status ===200) {
	      callback(this.response);
	    }
    }
    request.open("GET", path);
    request.send();
}

function showPie(response){
	let res = JSON.parse(response);
	Plotly.newPlot(res.div, res.data, res.layout)
}

function pieColor(){
	let yearInt = document.getElementById('inputYear');
		document.getElementById('yearGraph').style = "display: inline";
		document.getElementById('table').style = "display: inline";
		let data = JSON.stringify(yearInt.value);
		ajaxPostRequest('/send', data, showPie);
		document.getElementById('fetching').style = "visibility: visible";
		document.getElementById('fetching').innerHTML = "Fetching...";
		setTimeout(colorChange, 400);
		document.getElementById('table').style ='display: none';
		document.getElementById('yearGraph').style ='display: inline';
		document.getElementById('pieBTN').style = 'border: 2px solid #4CAF50;'
		document.getElementById('tableBTN').style = 'border: default';
		document.getElementById('divgraph').style ='display: inline';
}

function tableColor(){
	document.getElementById('table').style ='display: inline'
	document.getElementById('yearGraph').style ='display: none'
	document.getElementById('tableBTN').style = 'border: 2px solid #4CAF50;'
	setTimeout(colorChange, 800);
	document.getElementById('pieBTN').style = 'border: default'
	document.getElementById('divgraph').style ='display: inline'
}

function showTable(response){
	let res = JSON.parse(response);
	Plotly.newPlot('table', res[0], res[1]);
}

function sendYear(value){   
		let data = JSON.stringify(value);
		ajaxPostRequest('/send', data, showPie);
}

function colorChange(){
	document.getElementById('fetching').style = "visibility: hidden";
	document.getElementById('prompt').style.color = "black";
}

function ajaxPostRequest(path, data, callback){
    let request = new XMLHttpRequest();
    request.onreadystatechange = function(){
        if (this.readyState === 4 && this.status === 200){
            callback(this.response);
        }
    };
    request.open("POST", path);
    request.send(data);
}

function dropBTN(year){
	document.getElementById('dropbtn').innerHTML = string(year);
}


//Plotly.purge(/* graph element or graph id */)
//document.getElementById("myBtn").disabled = true
//display = none