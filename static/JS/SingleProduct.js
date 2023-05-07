// single product
function selectFirstImage () {
    let image = document.getElementById('first').getAttribute('src');
    show(image); 
  }
  function selectSecondImage () {
    let image = document.getElementById('second').getAttribute('src');
    show(image); 
  }
  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  async function show(image) {
    for (var i=0; i<=100; i++){
      document.getElementById("show").style.opacity = 1-(i/100);
      await sleep(5);
    }
    document.getElementById('show').src = image;
    for (var i=0; i<=100; i++){
      document.getElementById("show").style.opacity = i/100;
      await sleep(5);
    }
  }
  
  function increment () {
    document.getElementById('productQuantity').stepUp();
  }
  function decrement () {
    if (parseInt(document.getElementById('productQuantity').value) > 1)
      document.getElementById('productQuantity').stepDown();
  }
  
  function descriptionTab () {
    document.getElementById('comment').style.display = "none";
    document.getElementById('description').style.display = "block";
  }
  
  function commentTab () {
    document.getElementById('description').style.display = "none";
    document.getElementById('comment').style.display = "block";
  }