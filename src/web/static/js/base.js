function post(url, data) {
  fetch(url, {
    method: "POST",
    body: JSON.stringify(data)
  }).then(response => {
    if (response.status < 400) {
      return;
    }
    alert("Saving the document failed!");
  })
}
