// Change button title when a file is selected
var inputs = document.querySelectorAll('#image-input');
Array.prototype.forEach.call( inputs, function(input) {
    var label = input.nextElementSibling;
    var labelVal = label.innerHTML;
    input.addEventListener('change', function(e) {
        if (this.files && this.files.length > 0) {
            label.innerHTML = "1 FILE SELECTED";
        } else {
            label.innerHTML = labelVal;
        }
    });
});

$(document).ready(function() {
    // Load initial content
    load_content();
    // Refresh content every 30 seconds
    setInterval(load_content, 30000);
})

function load_content() {
    $.ajax({
        url: "/content",
        type: "get",
        success: function(response) {
            $("#content-container").html(response);
        }
    });
}