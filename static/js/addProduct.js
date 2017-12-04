
$(function(){
    $('#btnAddProd').click(function(){
        
        $.ajax({
            url: '/addProduct',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response){
                console.log(response);
            },
            error: function(error){
                console.log(error);
            }
        });
    });
});