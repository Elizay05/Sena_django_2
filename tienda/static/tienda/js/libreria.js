console.log("Hola mundo...!")
//alert("Hola mundo!!")

function eliminar(url){
    if(confirm("Está seguro?")){
        location.href = url;
    }
}

function remove_producto(url){
    location.href = url;
}

function add_carrito(url, id_producto){
    csrf_token = $("[name='csrfmiddlewaretoken']")[0].value;
    id = $(`#id_${id_producto}`).val()
    cantidad = $(`#cantidad_${id_producto}`).val()

    // Capturo referencia a dom de carrito del offCanvas
    contenido = $("#respuesta_carrito")
    loader = $("#loader")

    loader.removeClass("d-none");
    loader.addClass("d-block");

    offCanvas_carrito = $("#offcanvasRight");
    offCanvas_carrito.offcanvas('toggle');

    $.ajax({
        url: url,
        type: "POST",
        data: {"csrfmiddlewaretoken": csrf_token, "id": id, "cantidad": cantidad}
    })
    .done(function(respuesta){

        if (respuesta != "Error"){

            loader.removeClass("d-block");
            loader.addClass("d-none");
            // Pintar respuesta en offCanvas
            contenido.html(respuesta);
        }
        else{
            location.href="/tienda/inicio/";
        }
    })
    .fail(function(respuesta){
        location.href="/tienda/inicio/";
    });
}


function ver_carrito(url){
    // Capturo referencia a dom de carrito del offCanvas
    contenido = $("#respuesta_carrito")
    loader = $("#loader")

    loader.removeClass("d-none");
    loader.addClass("d-block");

    offCanvas_carrito = $("#offcanvasRight");
    offCanvas_carrito.offcanvas('toggle');

    $.ajax({
        url: url
    })
    .done(function(respuesta){

        if (respuesta != "Error"){
            /*setTimeout(()=>{
                loader.removeClass("d-block");
                loader.addClass("d-none");
                // Pintar respuesta en offCanvas
                contenido.html(respuesta);
            }, 3000);*/

            loader.removeClass("d-block");
            loader.addClass("d-none");
            // Pintar respuesta en offCanvas
            contenido.html(respuesta);

        }
        else{
            location.href="/tienda/inicio/";
        }
    })
    .fail(function(respuesta){
        location.href="/tienda/inicio/";
    });
}