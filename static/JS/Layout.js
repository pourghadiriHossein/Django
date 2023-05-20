// Public Part
// Get Top Bar Date Time
let date = new Date();
customizeDate = 
" سال : "+date.getFullYear()+" ماه : "+ date.getMonth()+" روز :‌ "+date.getDate()
+" "+" ساعت : "+date.getHours()+" دقیقه : "+date.getMinutes();
document.getElementById('customizeDate').innerHTML = customizeDate;

//Scroll to Top of Document Page Part 
//Get the button
var mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}
window.addEventListener("onscroll", ()=> {
	document.getElementById("Result").innerHTML = 55;
});
// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}