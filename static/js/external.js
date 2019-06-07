// detect title entry in input field
function changeBookTitleHandler() {
  var title = document.getElementById('title').value

  if (title != "")
    document.getElementById('submit').disabled = false
  else
    document.getElementById('submit').disabled = true

}

// prevent empty title
document.addEventListener("DOMContentLoaded", function(event) {
  var submitButton = document.getElementById('submit')

  if (submitButton)
    changeBookTitleHandler()
});