/**
 * Created by JoaoCosta on 20/03/16.
 */

define(['core/context'], function(Context){

    function getContext(){
        return Context;
    }

    function initProcessingControllers(){
        require(['processing/imageLoad'], function(ImageLoadController){
            console.log("estou no manager");
            ImageLoadController.init();
        });
    }

    return{
        getContext:                     getContext,
        initProcessingControllers:      initProcessingControllers
    }
});