var auth_string = ""

window.addEventListener('load', function() {
	// set active link based on page title
	var title = $('title').text();
	var links = $('.nav-link');
	if(title.includes("IDV")) {
		links[0].parentElement.classList.add("active");
	} else if (title.includes("KBA Form")) {
		links[1].parentElement.classList.add("active");
	};
})

window.addEventListener('load', function() {
	var cognito_resp = generateCognitoToken(function(resp) {
		// console.log(resp);
		if ("error" in resp) {
			alert("Cognito Token Generation Failed");
			return false;
		}
		auth_string = "Bearer " + resp["access_token"];
	});
	return cognito_resp;
});

// Baisc JS to validate form entry
(function() {
	'use strict';
	window.addEventListener('load', function() {
	// Fetch all the forms we want to apply custom Bootstrap validation styles to
		var forms = document.getElementsByClassName('needs-validation');
		// Loop over them and prevent submission
		var validation = Array.prototype.filter.call(forms, function(form) {
			form.addEventListener('submit', function(event) {
			if (form.checkValidity() === false) {
				event.preventDefault();
				event.stopPropagation();
			}
			form.classList.add('was-validated');
			}, false);
		});
	}, false);
})();

$('#kba-form').submit(function(e) {
	e.preventDefault();

	var radios = document.getElementsByClassName("custom-control-input");

	payload = {};
	
	for (var i = 0; i <= radios.length - 1; i++) {
		if (radios[i].checked) {
			var parsedAnswer = (radios[i].id).split('-c');
			questionNumber = parsedAnswer[0];
			kbaAnswer = parsedAnswer[1];
			payload["outWalletAnswer" + questionNumber] = kbaAnswer;
		}
	}

	// show the error page manually
	// if the last selection on the page is chosen
	var showFailed = false;
	if(payload['outWalletAnswer5'] == 5) {
		showFailed = true;
	}

	// console.log(payload);
	$.ajax({
 		url: "https://pv48iufl8k.execute-api.us-west-1.amazonaws.com/Test/kba-post",
 		type: "POST",
  		contentType: "application/json",
 		headers: {
 		    "Authorization": auth_string
 		},
 		data : JSON.stringify({"answers":payload}),
 		success: function(resp){
 			redirectFromKba(resp, showFailed);
 		},
 		error: function(XMLHttpRequest, textStatus, errorThrown) {
        	alert("Status: " + textStatus); alert("Error: " + errorThrown);
    	}
 	})

});

$('#user-info-form').submit(function(e) {
	e.preventDefault();
	var validationFailed = false;

	var form = document.getElementsByClassName('needs-validation')[0];
	if (form.checkValidity() === false) {
		validationFailed = true;
	}

	if (validationFailed) {
		e.preventDefault();
		e.stopPropagation();
		return false;
	}
	received = $('input');
	
 	var firstName = $('input#firstName').val();
 	var lastName = $('input#lastName').val();
 	var middleInitial = $('input#middleInitial').val();
 	var address = $('input#address').val();
 	var address2 = $('input#address2').val();
 	var city = $('input#city').val();
 	var state = $('select#state').val();
 	var postal = $('input#zip').val();
 	var ssn = $('input#ssn').val();
 	var dob = $('input#dob').val();

 	var userInfo = {
 		"firstName" : firstName,
 		"lastName" : lastName,
 		"middleInitial" : middleInitial,
 		"address" : address,
 		"address2" : address2,
 		"city" : city,
 		"state" : state,
 		"postal" : postal,
 		"ssn" : ssn,
 		"dob" : dob,	
 	};

 	$.ajax({
 		url: "https://pv48iufl8k.execute-api.us-west-1.amazonaws.com/Test/pii-check-post",
 		type: "POST",
  		contentType: "json",
 		headers: {
 		    "Authorization": auth_string
 		},
 		data : JSON.stringify({"user_info":userInfo}),
 		success: function(resp){
 			alert("User " + firstName + " authenticated");
 			redirectToKba(resp);
 		},
 		error: function(XMLHttpRequest, textStatus, errorThrown) {
        	alert("Status: " + textStatus); alert("Error: " + errorThrown);
    	}
 	})
});

function generateCognitoToken(callback) {
	var clientId = "5q9usbn2uunrpbjo9h4celtknv";
	var clientSecret = "t3pidsk30e7oruthjpcel4rjlvvoqm9fkgadtub654n3c20gt9b";

	var clientString = clientId + ":" + clientSecret;
	var encoded = btoa(clientString);

	var headerString = "Basic " + encoded;

	$.ajax({
		url: "https://test-api-gw-auth.auth.us-east-1.amazoncognito.com/oauth2/token",
		type: "POST",
		data: "grant_type=client_credentials",
		async: false,
		headers: {
			"Content-Type": "application/x-www-form-urlencoded",
			"Authorization": headerString
		},
		success: function(resp){
			// console.log(JSON.stringify(resp));
			callback(resp);
			return resp;
		},
		error: function(XMLHttpRequest, textStatus, errorThrown) {
        	alert("Status: " + textStatus); alert("Error: " + errorThrown);
    	}
	});
};

function redirectToKba(resp) {
	var st = JSON.stringify(resp);
	var origin = location.origin
	var url = origin + '/kba-questions';

	var form = document.createElement("form");
	form.setAttribute("action", url);
	form.setAttribute("method", "post");
	form.setAttribute("style", "display:none")
	form.setAttribute("id", "kba");

	var kba = document.createElement("input");
	kba.setAttribute("type", "text");
	kba.setAttribute("name", "payload");
	kba.setAttribute("value", st)
	
	form.appendChild(kba);
	$('body').append(form);
	form.submit();
}

function redirectFromKba(resp, showFailed) {
	var origin = location.origin;
	var form = document.createElement("form");
	var url = ''
	form.setAttribute("method", "post");
	form.setAttribute("style", "display:none")

	if(showFailed) {
		var url = origin + '/kba-failed';
	} else if (resp.includes("success")) {
		var url = origin + '/kba-success';
		var st = JSON.stringify(resp);
		var kbaResp = document.createElement("input");
		kbaResp.setAttribute("type", "text");
		kbaResp.setAttribute("name", "payload");
		kbaResp.setAttribute("value", st)
	} else {
		var url = origin + '/kba-failed';
	}

	form.setAttribute("action", url);
	$('body').append(form);
	form.submit();
}
