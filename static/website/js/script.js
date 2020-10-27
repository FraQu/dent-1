$(document).ready(function() {
    $('.nav-button').click(function() {
    $('.nav-button').toggleClass('change');
    });
});

function load_add_customer() {
     document.getElementById("body_content").innerHTML='<object type="text/html" data="templates/website/add_customer.html" ></object>';
}