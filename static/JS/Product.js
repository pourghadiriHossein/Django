//Product
//select Mode Part
function selectMode() {
    var select = document.getElementById('sort');
    var value = select.options[select.selectedIndex].value;
    switch(value) {
      case '1': 
        oldest();
        break;
      case '2': 
        newest();
        break;
      case '3':
        cheapest();
        break;
      case '4':
        expensivest();
        break;      
    }
  }
  function oldest() {
    var main = document.getElementById( 'productBox' );
    [].map.call( main.children, Object ).sort( function ( a, b ) {
        return +a.id.match( /\d+/ ) - +b.id.match( /\d+/ );
    }).forEach( function ( elem ) {
        main.appendChild( elem );
    });
    document.getElementById('counter').innerHTML = main.children.length;
  }
  function newest() {
    var main = document.getElementById( 'productBox' );
    [].map.call( main.children, Object ).sort( function ( a, b ) {
        return +b.id.match( /\d+/ ) - +a.id.match( /\d+/ );
    }).forEach( function ( elem ) {
        main.appendChild( elem );
    });
    document.getElementById('counter').innerHTML = main.children.length;
  }
  function cheapest() {
    var main = document.getElementById( 'productBox' );
    [].map.call( main.children, Object ).sort( function ( a, b ) {
        return +a.dataset.price.match( /\d+/ ) - +b.dataset.price.match( /\d+/ );
    }).forEach( function ( elem ) {
        main.appendChild( elem );
    });
    document.getElementById('counter').innerHTML = main.children.length;
  }
  function expensivest() {
    var main = document.getElementById( 'productBox' );
    [].map.call( main.children, Object ).sort( function ( a, b ) {
        return +b.dataset.price.match( /\d+/ ) - +a.dataset.price.match( /\d+/ );
    }).forEach( function ( elem ) {
        main.appendChild( elem );
    });
    document.getElementById('counter').innerHTML = main.children.length;
  }

  //Search Part
  function searchProduct() {
    let products = document.getElementsByClassName('imageBox');
    let search = document.getElementById('searchBox').value;
    let counter = 0;
    for (let i = 1; i < products.length; i++){
      products[i].style.display = "inline-block";
      counter ++;
    }
    for(let i = 0; i < products.length; i++) {
      if(products[i].dataset.name.match(search)){
        products[i].style.display = "inline-block";
        counter ++;
      }
      else 
        products[i].style.display = "none";  
    }
    document.getElementById('counter').innerHTML = counter;
  }


  //pagination
  
  let numberOfProductInEachPage = 6;
  let allProducts = document.getElementsByClassName('imageBox');
  let numberOfPageButton = Math.ceil(allProducts.length / numberOfProductInEachPage);
  let allPage = document.getElementById('pagination');
  
  const newButton = (index) => {
    const pageNumber  = document.createElement("a");
    pageNumber.innerHTML = index;
    pageNumber.setAttribute("id", index);
    pageNumber.setAttribute("class", 'BTN'+index+'');
    pageNumber.setAttribute('onclick', 'selectedPage( " '+index+' " )');
    allPage.appendChild(pageNumber);
  }
  const getPaginationNumbers = () => {
    for (let i = numberOfPageButton ; i > 0 ; i--){
      newButton(i);
    }
  }  
  let selectedPage = (pageIndex) => {
    maxProductIndex = pageIndex * numberOfProductInEachPage;
    minProductIndex = maxProductIndex - numberOfProductInEachPage;
    if(maxProductIndex > allProducts.length)
      maxProductIndex = allProducts.length;
    for (let i = 0; i < allProducts.length; i++){
      allProducts[i].style.display = "none";
    }
    let counter = 0
    for (let j = minProductIndex; j < maxProductIndex; j++){
      allProducts[j].style.display = "inline-block";
      counter ++;
    }
    document.getElementById('counter').innerHTML = counter;
  }

  
  window.addEventListener("load", () => {
    getPaginationNumbers();
    selectedPage(1);
    document.getElementById('counter').innerHTML = 6;
  });