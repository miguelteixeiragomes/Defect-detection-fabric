/**
 * Created by JoaoCosta on 20/03/16.
 */

define(function(){
    "use strict";

    var imageLoadController;

    function setImageLoadController(controller){
        imageLoadController = controller;
    }

    function getImageLoadController()
    {
        return imageLoadController;
    }

    return{
        setImageLoadController:   setImageLoadController,
        getImageLoadController:   getImageLoadController
    }
});