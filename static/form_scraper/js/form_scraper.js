hideloader();
const myForm = document.getElementById("myForm");
document.getElementById("stop").disabled=true;

var selected = [];

function stop() {
	query=get_query();
	fetch('/api/stop'+'?query=' + query);
}

async function triggercsv(csvFile) {
	const formData = new FormData();

	formData.append('csvFile', csvFile);

	await fetch('/api/csv', {
		method: 'POST',
		body: formData
	});
	// .then((response) => response.json())
	// .then((result) => {
	//   console.log('Success:', result);
	// })
	// .catch((error) => {
	//   console.error('Error:', error);
	// });
}


async function contact(details) {

	total = selected.length;
	showloader();
	for (i = 0; i < total; i++) {
		row_id = 'row' + selected[i].toString()
		document.getElementById(row_id).style.backgroundColor = 'hsl(60,60%,85%)';
		const formData = new FormData();
		link_id = 'link' + selected[i].toString()
		link = link = document.getElementById(link_id);
		formData.append('urls', link.href);
		formData.append('details', JSON.stringify(details));

		await fetch('/api/contact', {
			method: 'POST',
			body: formData
		})
			.then((response) => response.json())
			.then((result) => {
				console.log('Success:', result);
				if (result['status'] == 'success') {
					document.getElementById(row_id).style.backgroundColor = 'hsl(120,60%,85%)';
				}
				else {
					document.getElementById(row_id).style.backgroundColor = 'hsl(0,60%,85%)';
				}

			})
			.catch((error) => {
				console.error('Error:', error);
			});
	}
	hideloader();

}

function toggle(source) {
	checkboxes = document.getElementsByName('foo');
	for (var i = 0, n = checkboxes.length; i < n; i++) {
		checkboxes[i].checked = source.checked;
		selected_rows(checkboxes[i])
	}
}

function selected_rows(source) {


	if (source.checked) {
		selected.push(source.id)
	}

	else {
		const index = selected.indexOf(source.id);
		selected.splice(index, 1)

	}
}

async function contact_rows(source) {

	var details = {
		"first_name": document.getElementById("first_name").value,
		"last_name": document.getElementById("last_name").value,
		"full_name": document.getElementById("full_name").value,
		"company_name": document.getElementById("company_name").value,
		"company_website": document.getElementById("company_website").value,
		"address": document.getElementById("address").value,
		"city": document.getElementById("city").value,
		"state": document.getElementById("state").value,
		"zip_code": document.getElementById("zip_code").value,
		"subject": document.getElementById("subject").value,
		"email": document.getElementById("email").value,
		"message": document.getElementById("message").value,
		"phone": document.getElementById("phone").value,
	}

	showloader();

	row_id = 'row' + (source.id).toString()
	document.getElementById(row_id).style.backgroundColor = 'hsl(60,60%,85%)';
	const formData = new FormData();
	link_id = 'link' + (source.id).toString()
	link = link = document.getElementById(link_id);
	formData.append('urls', link.href);
	formData.append('details', JSON.stringify(details));

	await fetch('/api/contact', {
		method: 'POST',
		body: formData
	})
		.then((response) => response.json())
		.then((result) => {
			console.log('Success:', result);
			if (result['status'] == 'success') {
				document.getElementById(row_id).style.backgroundColor = 'hsl(120,60%,85%)';
			}
			else {
				document.getElementById(row_id).style.backgroundColor = 'hsl(0,60%,85%)';
			}

		})
		.catch((error) => {
			console.error('Error:', error);
		});

	hideloader();
}

details.addEventListener("submit", function (e) {
	e.preventDefault();
	var details = {
		"first_name": document.getElementById("first_name").value,
		"last_name": document.getElementById("last_name").value,
		"full_name": document.getElementById("full_name").value,
		"company_name": document.getElementById("company_name").value,
		"company_website": document.getElementById("company_website").value,
		"address": document.getElementById("address").value,
		"city": document.getElementById("city").value,
		"state": document.getElementById("state").value,
		"zip_code": document.getElementById("zip_code").value,
		"subject": document.getElementById("subject").value,
		"email": document.getElementById("email").value,
		"message": document.getElementById("message").value,
		"phone": document.getElementById("phone").value,
	}

	contact(details)
});

myForm.addEventListener("submit", function (e) {
	e.preventDefault();
	selected = [];
	var csvFile = document.getElementById("csvFile").files[0];
	showloader();
	const api_url = "/api/";
	const api_url1 = "/api/results";
	const api_url2 = "/api/queries";

	triggercsv(csvFile);

	setTimeout(() => { getapi(api_url1, api_url2, true); }, 1000);

});

search_form.addEventListener("submit", function (e) {
	e.preventDefault();
	mysearch();
});

// Defining async function

function get_query() {
	var query = document.getElementById('my_query').value;
	const country = document.getElementById('country').value;
	const zip = document.getElementById('zip').value;

	if (country) {
		query += " in " + country;
	}
	if (zip) {
		query += " " + zip;
	}
	return query
}

async function triggerapi(url) {


	var query = get_query();
	var searches = document.getElementById('searches').value;
	const response = await fetch(url + '?query=' + query + '&number=' + searches);
}
async function getapi(url1, url2, is_file) {

	if (is_file == true) {
		var query = 'file'
	}
	else {
		var query = get_query();
	}


	if (query) {
		document.getElementById('head').textContent = "Search Results for: " + query;


		// Storing response
		const response = await fetch(url1 + '?query=' + query);

		// Storing data in form of JSON
		var data = await response.json();
		show(data);

		const response2 = await fetch(url2 + '?query=' + query);
		// Storing data in form of JSON
		var data2 = await response2.json();

		if (data2[0].in_process) {
			var current_progress = Math.round(data2[0].progress);
			var progress_string = current_progress.toString();

			document.getElementById('search_progress').style.width = progress_string + "%"
			setTimeout(() => { getapi(url1, url2, is_file); }, 1000);

		}
		else {
			document.getElementById('search_progress').style.width = "100%"
			hideloader();
		}
	}
	else {
		hideloader();
	}


}

function mysearch() {
	showloader();
	selected = [];
	const api_url = "/api/";
	const api_url1 = "/api/results";
	const api_url2 = "/api/queries";
	triggerapi(api_url);

	setTimeout(() => { getapi(api_url1, api_url2, false); }, 1000);

}

function csvsearch() {
	console.log("working")
}

function hideloader() {
	document.getElementById('loading').style.display = 'none';
	document.getElementById("stop").disabled=true;
	document.getElementById("start_button").disabled=false;
	document.getElementById("my_query").disabled=false;
	document.getElementById("searches").disabled=false;
	document.getElementById("search_progress").className = "progress-bar bg-success"
}

function showloader() {
	document.getElementById('loading').style.display = 'inline';
	document.getElementById("stop").disabled=false;
	document.getElementById("start_button").disabled=true;
	document.getElementById("my_query").disabled=true;
	document.getElementById("searches").disabled=true;
	document.getElementById("search_progress").className = "progress-bar progress-bar-striped progress-bar-animated bg-warning"
}
function hidehead() {
	document.getElementById('head').style.display = 'none';
}

function showhead() {
	document.getElementById('head').style.display = 'inline';
}

// Function to define innerHTML for HTML table
function show(data) {

	let tab = `<thead>
		<tr>
			<td><input type="checkbox" onClick="toggle(this)" id="allcb" name="allcb"/></td>
			<td>Serial</td>
			<td>Contact URL</td>
			<td>Domain</td>
			<td>Active</td>
			<td style="float: right">Action</td>
		</tr>
	</thead>`

	tab += '<tbody>'
	// Loop to access all rows
	i = 1
	for (let r of data) {
		tab += `<tr id="row${i}">
    <td><input type="checkbox" onClick="selected_rows(this)" id="${i}" name="foo"/></td>
    <td>${i} </td>
	<td><a id="link${i}" href="${r.contact_url}">${r.contact_url}</a></td>
	<td><a href="${r.domain}">${r.domain}</a></td>
	<td>
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="green" class="bi bi-vinyl-fill" viewBox="0 0 16 16">
            <path d="M8 6a2 2 0 1 0 0 4 2 2 0 0 0 0-4zm0 3a1 1 0 1 1 0-2 1 1 0 0 1 0 2z"/>
            <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM4 8a4 4 0 1 0 8 0 4 4 0 0 0-8 0z"/>
        </svg>
    </td>
	<td>
        <button onClick="contact_rows(this)" id="${i}" class="btn" style="float: right">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="#195173" class="bi bi-send" viewBox="0 0 16 16">
                <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576 6.636 10.07Zm6.787-8.201L1.591 6.602l4.339 2.76 7.494-7.493Z"/>
            </svg>
        </button>
    </td>		
</tr>`;
		i++;
	}
	tab += '</tbody>'
	// Setting innerHTML as tab variable
	document.getElementById("resultTable").innerHTML = tab;

}
