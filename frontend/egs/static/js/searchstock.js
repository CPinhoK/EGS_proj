// shows all products of the database to item.html
async function getproducts(url) {
    const response = await fetch(url);
    var data = await response.json();
    console.log(data);
    showallproducts(data);
}

// Function to define innerHTML for all products
function showallproducts(data) {
    let allproducts = '';
    for (let product of data){
        allproducts += `
        <div class="col-md-4 col-xs-6">
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
            </div>
        </div>`;
    }
    // Setting innerHTML as tab variable
    document.getElementById("allproducts").innerHTML = allproducts;
}

getproducts('http://127.0.0.1:8000/products')