// // Script to open and close sidebar
// function w3_open() {
//     document.getElementById("mySidebar").style.display = "block";
//     document.getElementById("myOverlay").style.display = "block";
// }

// function w3_close() {
//     document.getElementById("mySidebar").style.display = "none";
//     document.getElementById("myOverlay").style.display = "none";
// }

// // Modal Image Gallery
// function onClick(element) {
//     document.getElementById("img01").src = element.src;
//     document.getElementById("modal01").style.display = "block";
//     var captionText = document.getElementById("caption");
//     captionText.innerHTML = element.alt;
// }

// document.getElementById('textFileUpload').addEventListener('change', function(event) {
//     const file = event.target.files[0];
//     if (file && file.type === 'text/plain') {
//         const reader = new FileReader();
//         reader.onload = function(e) {
//             // Store the description text in a global variable
//             window.descriptionText = e.target.result;
//         };
//         reader.readAsText(file);
//     } else {
//         alert('Please upload a valid text file.');
//     }
// });
