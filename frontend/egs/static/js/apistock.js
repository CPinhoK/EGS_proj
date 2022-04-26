//const api_url = '';

async function getapi(url) {
    const response = await fetch(url);

    var data = await response.json();
    console.log(data);
    if(response){
        //hideLoader();
    }
    show(data);

}

getapi('http://127.0.0.1:8000/products')

// Function to hide the loader
function hideLoader() {
    document.getElementById('loading').style.display = 'none';
}
// Function to define innerHTML for HTML table
function show(data) {
    for (let product of data){
        tab = `<div class="product">
        <div class="product-img">
        <img src="${product.image}" alt="">
            <div class="product-label">
                <span class="sale">-30%</span>
                <span class="new">NEW</span>
            </div>
        </div>
        <div class="product-body">
            <p class="product-category">${product.category}</p>
            <h3 class="product-name"><a href="#">${product.name}</a></h3>
            <h4 class="product-price">{product.price}<del class="product-old-price">{{product.price}}</del></h4>
            <div class="product-rating">
                <i class="fa fa-star"></i>
                <i class="fa fa-star"></i>
                <i class="fa fa-star"></i>
                <i class="fa fa-star"></i>
                <i class="fa fa-star"></i>
            </div>
            <div class="product-btns">
                <button class="add-to-wishlist"><i class="fa fa-heart-o"></i><span class="tooltipp">add to wishlist</span></button>
                <button class="add-to-compare"><i class="fa fa-exchange"></i><span class="tooltipp">add to compare</span></button>
                <button class="quick-view"><i class="fa fa-eye"></i><span class="tooltipp">quick view</span></button>
            </div>
        </div>
        <div class="add-to-cart">
            <button class="add-to-cart-btn"><i class="fa fa-shopping-cart"></i> add to cart</button>
        </div>
    </div>`;
    }
    // Setting innerHTML as tab variable
    document.getElementById("products").innerHTML = tab;
}