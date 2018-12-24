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