//const api_url = '';

//shows the last 4 products of the database to index.html
async function newestproducts(url){
    const response = await fetch(url);
    var data = await response.json();
    console.log(data.slice(-4));
    shownewproducts(data.slice(-4));
}

// Function to define innerHTML for new products
function shownewproducts(data) {
    let newproduct = '';
    for (let product of data){
        newproduct += `
        <div class="product">
            <div class="product-img">
                <img src="${product.image}" alt="">
                <div class="product-label">
                    <span class="new">NEW</span>
                </div>
            </div>
            <div class="product-body">
                <p class="product-category">${product.category.name}</p>
                <h3 class="product-name"><a href="#">${product.name}</a></h3>
                <h4 class="product-price">${product.price}</h4>
            </div>
            <div class="add-to-cart">
                <button class="add-to-cart-btn"><i class="fa fa-shopping-cart"></i> add to cart</button>
            </div>
        </div>`;
    }
    // Setting innerHTML as tab variable
    document.getElementById("newproducts").innerHTML = newproduct;
}

newestproducts('http://127.0.0.1:8000/products')
