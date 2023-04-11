var allMenuListBtn = document.getElementsByClassName("list-btn");
var i;

for (i = 0; i < allMenuListBtn.length; i++) {
    allMenuListBtn[i].addEventListener("click", function() {
        var content = this.nextElementSibling;
        var state =  content.getAttribute('class');
        if (state === "items-after-click" || state === "items") {
            for (button of allMenuListBtn) {
                button.style.color = "white";
                var allContent = button.nextElementSibling;
                allContent.removeAttribute("class");
                allContent.setAttribute('class', 'items-after-click');
            }
            this.style.color = "#0f4857";
            content.removeAttribute("class");
            content.setAttribute('class', 'items-befor-click');
        } 
  });
}
const allContent = document.querySelectorAll('[data-type="content"]');
const showContent = (contentName) => {
    let requestElement = document.getElementById(contentName);
    allContent.forEach((currentElement) => {
        var state =  currentElement.getAttribute('class');
        if (state == 'content-visible') {
            currentElement.removeAttribute('class');
            currentElement.setAttribute('class', 'content-hidden');
        }
    });
    setTimeout(() => {
        requestElement.removeAttribute('class');
        requestElement.setAttribute('class', 'content-visible');
    },1000);
}
window.addEventListener('load', ( )=> {
    let requestElement = document.getElementById('content-profile');
    requestElement.removeAttribute('class');
    requestElement.setAttribute('class', 'content-visible');
});

const openDialogBox = (dialogBox) => {
    let selectedDialogBox= document.getElementById(dialogBox);
    selectedDialogBox.style.display = "block";
}
const closeDialogBox = (dialogBox) => {
    let selectedDialogBox= document.getElementById(dialogBox);
    selectedDialogBox.style.display = "none";
}