console.log("Working fine");
const monthNames = ["Jan", "Feb", "Mar", "April", "May", "June",
    "July", "Aug", "Sept", "Oct", "Nov", "Dec"
];

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Check if the cookie name matches
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


$("#commentForm").submit(function (e) {
    e.preventDefault(); // Prevents the default form submission
    let date = new Date();
    let time = date.getDay() + " " + monthNames[date.getMonth()] + ", " + date.getFullYear()

    
    $.ajax({
        data:$(this).serialize(),
        method:$(this).attr("method"),
        url: $(this).attr("action"), 
        dataType:"json",
        success: function(res){
            console.log("Comment, saved to db");

            if(res.bool == true){
                $("#review-response").html("Review added successfuly!");
                $(".hide-comment-form").hide();
                $(".add-review").hide();

                let _html = '<div class="single-comment justify-content-between d-flex mb-30">'
                _html += '<div class="user justify-content-between d-flex">'
                _html += '<div class="thumb text-center">'
                _html += '<img src="https://thumbs.dreamstime.com/b/default-avatar-profile-vector-user-profile-default-avatar-profile-vector-user-profile-profile-179376714.jpg" alt="" />'
                _html += '<a href="#" class="font-heading text-brand">' + res.context.user + '</a>'
                _html += '</div>'

                _html += '<div class="desc">'
                _html += '<div class="d-flex justify-content-between mb-10">'
                _html += '<div class="d-flex align-items-center">'
                _html += '<span class="font-xs text-muted">' + time + ' </span>'
                _html += '</div>'

                for (var i = 1; i <= res.context.rating; i++) {
                    _html += '<i class="fa fa-star text-warning"></i>';
                }


                _html += '</div>'
                _html += '<p class="mb-10">' + res.context.review + '</p>'

                _html += '</div>'
                _html += '</div>'
                _html += ' </div>'

                $(".comment-list").prepend(_html)

                            


            }

            

         }

        })  
})            
 
$(document).ready(function (){
    $(".filter-checkbox, #price-filter-btn").on("click", function () {
        console.log("A checkbox have been clicked");

        let filter_object = {}

        let min_price = $("#max_price").attr("min")
        let max_price = $("#max_price").val()

        filter_object.min_price = min_price;
        filter_object.max_price = max_price;

        $(".filter-checkbox").each(function () {
            let filter_value = $(this).val()
            let filter_key = $(this).data("filter") // vendor, category

            // console.log("Filter value is:", filter_value);
            // console.log("Filter key is:", filter_key);

            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter=' + filter_key + ']:checked')).map(function (element) {
                return element.value
            })
        })
        console.log("Filter Object is: ", filter_object);
        $.ajax({
            url: '/filter-products',
            data: filter_object,
            dataType: 'json',
            beforeSend: function () {
                console.log("Trying to filter product...");
            },
            success: function (response) {
                console.log(response.length);
                console.log("Data filtred successfully...");
                // $(".totall-product").hide()
                $("#filtered-product").html(response.data)
            }
        })
    });

    $("#max_price").on("blur", function () {
        let min = $(this).attr("min")
        let max = $(this).attr("max")
        let current_price = $(this).val()

        console.log("Current Price is:", current_price);
        console.log("Max Price is:", max);
        console.log("Min Price is:", min);

        if (current_price < parseInt(min) || current_price > parseInt(max)) {

            min = Math.round(min * 100) / 100
            max_price = Math.round(max * 100) / 100


            console.log("Max Price is:", max);
            console.log("Min Price is:", min);

            alert("Price must between kshs." + min + ' and kshs.' + max)
            $(this).val(min)
            $('#range').val(min)

            $(this).focus()

            return false

        }

    })

    // Adding to Cart logic

    // $("#add-to-cart-btn").on("click", function () {

    //     let quantity = $("#product-quantity-").val()
    //     let productTitle =  $(".productTitle-").val()
    //     let productId = $(".product-productId-").val()
    //     let productPrice = $(".curr-prod-price-").text()
    //     let this_val = $(this)

    //     console.log("quantity", quantity);
    //     console.log("productTitle", productTitle);
    //     console.log("productId", productId);
    //     console.log("productPrice", productPrice);
    //     console.log("this_val", this_val);

    //     $.ajax({
    //         url: '/add-to-cart',
    //         data: {
    //             'id': productId,
    //             'qty': quantity,
    //             'title': productTitle,
    //             'price': productPrice,
    //         },

    //         dataType:'json',
    //         beforeSend: function(){
    //             // console.log("Wait adding product to cart...");

    //         },
    //         success: function(res){
    //             this_val.html( "Added to cart" );
    //             console.log("Successfuly added product to cart.");
    //             $(".cartItemsCount").text(res.cartTotalItems)
    //         }
    //     })
       
           
    // })

     $(".add-to-cart-btn").on("click", function () {
        let this_val = $(this)
        let index_data = this_val.attr("data-index")

        let quantity = $(".product-quantity-" + index_data).val()
        let productTitle =  $(".product-title-" + index_data).val()
        let productid = $(".product-id-" + index_data).val()
        let productId = $(".product-productId-" + index_data).val()
        let productPrice = $(".curr-prod-price-" + index_data).text()
        let productImage = $(".product-image-" + index_data).val()

        

        console.log("quantity", quantity);
        console.log("productTitle", productTitle);
        console.log("productId", productId);
        console.log("productPrice", productPrice);
        console.log("productid", productid);
        console.log("productImage", productImage);
        console.log("index_data", index_data);
        console.log("this_val", this_val);



        $.ajax({
            url: '/add-to-cart',
            data: {
                'id': productid,
                'productId':productId,
                'qty': quantity,
                'title': productTitle,
                'price': productPrice,
                'img': productImage,
            },

            dataType:'json',
            beforeSend: function(){
                console.log("Wait adding product to cart...");

            },
            success: function(res){
                this_val.html( "✔" );
                console.log("Successfuly added product to cart.");
                $(".cartItemsCount").text(res.cartTotalItems)
            }
        })
       
           
    })

    // $("#add-to-cart-btn").on("click", function () {

    //     let quantity = $("#product-quantity").val()
    //     let productTitle =  $(".productTitle").val()
    //     let productId = $(".productId").val()
    //     let productPrice = $("#curr-prod-price").text()
    //     let this_val = $(this)

    //     console.log("quantity", quantity);
    //     console.log("productTitle", productTitle);
    //     console.log("productId", productId);
    //     console.log("productPrice", productPrice);
    //     console.log("this_val", this_val);

    //     $.ajax({
    //         url: '/add-to-cart',
    //         data: {
    //             'id': productId,
    //             'qty': quantity,
    //             'title': productTitle,
    //             'price': productPrice,
    //         },

    //         dataType:'json',
    //         beforeSend: function(){
    //             // console.log("Wait adding product to cart...");

    //         },
    //         success: function(res){
    //             // this_val.html( "Added to cart" );
    //             // console.log("Successfuly added product to cart.");
    //             $(".cartItemsCount").text(res.cartTotalItems)
    //         }
    //     })
       
           
    // })
    

    $(document).on("click", ".delete-product, .delete-item", function (e) {
        e.preventDefault();


        let product_id = $(this).attr("data-product")
        let this_val = $(this)

        console.log("ProductID:", product_id);

        $.ajax({
            url: "/delete-cart-item",
            data: {
                "id": product_id
            },
            headers: {
                'X-CSRFToken': getCookie('csrftoken')  // Include a function to get the CSRF token
            },
            dataType: "json",
            beforeSend: function () {
                // this_val.attr('disabled', true);
                this_val.hide()
            },
            success: function (response) {
                // console.log(response);

                this_val.show()
                $(".cartItemsCount").text(response.cartTotalItems)
                // this_val.attr('disabled', false);
                $("#async-cart-list").html(response.data)
            }
        })

    })

    $(document).on("click", ".update-product", function (e) {

        e.preventDefault();

        let product_id = $(this).attr("data-product")
        let this_val = $(this)
        let product_quantity = $(".product-qty-" + product_id).val()

        console.log("Product_id:", product_id);
        console.log("Product_quantity:", product_quantity);

        $.ajax({
            url: "/update-cart",
            data: {
                "id": product_id,
                "quantity": product_quantity,
            },
            dataType: "json",
            beforeSend: function () {
                this_val.hide()
            },
            success: function (response) {
                this_val.show()
                $(".cartItemsCount").text(response.cartTotalItems)
                $("#async-cart-list").html(response.data)
                window.location.reload()

            }
        })

    })



})


