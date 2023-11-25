$(document).ready(function () {
    // Handle "Add" and "Minus" buttons
    $(".quantity-adjust").click(function (e) {
      e.preventDefault();
      var pid = $(this).data("pid");
      var action = $(this).data("action");
  
      $.ajax({
        url: "/plus_cart/",
        data: {
          prod_id: pid,
          action: action,
        },
        method: "GET",
        success: function (data) {
          $("#quantity-" + pid).html(data.quantity);
          $("#amount").html(data.amount);
          $("#totalamount").html(data.totalamount);
        },
        error: function (error) {
          console.log(error);
        },
      });
    });
  
    // Handle "Remove" button
    $(".remove-from-cart").click(function (e) {
      e.preventDefault();
      var pid = $(this).data("pid");
  
      $.ajax({
        url: "/remove_cart/",
        data: {
          prod_id: pid,
        },
        method: "GET",
        success: function (data) {
          // Handle success, e.g., remove the cart item from the UI
          // You can refresh the page or update the UI as needed
          location.reload();
        },
        error: function (error) {
          console.log(error);
        },
      });
    });
  });
  