// Script to open and close sidebar
function w3_open() {
    document.getElementById("mySidebar").style.display = "block";
    document.getElementById("myOverlay").style.display = "block";
}

function w3_close() {
    document.getElementById("mySidebar").style.display = "none";
    document.getElementById("myOverlay").style.display = "none";
}

// Modal Image Gallery
function onClick(element) {
    document.getElementById("img01").src = element.src;
    document.getElementById("modal01").style.display = "block";
    var captionText = document.getElementById("caption");
    captionText.innerHTML = element.alt;
}

function generatePost() {
    // Get form elements
    var imageFile = document.getElementById('imageUpload').files[0];
    var description = document.getElementById('description').value;
    var campaignDays = document.getElementById('campaignDays').value;

    // Check if the form is valid
    if (!imageFile || !description || !campaignDays) {
        alert("Please fill in all fields.");
        return;
    }

    // Create a URL for the uploaded image
    var imageUrl = URL.createObjectURL(imageFile);

    // Set the preview elements
    document.getElementById('previewImage').src = imageUrl;
    document.getElementById('previewDescription').innerText = description;
    document.getElementById('previewDays').innerText = "Campaign Days: " + campaignDays;

    // Display the preview section
    document.getElementById('postPreview').style.display = 'block';
}
