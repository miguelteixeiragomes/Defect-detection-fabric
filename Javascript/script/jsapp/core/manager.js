/**
 * Created by JoaoCosta on 20/03/16.
 */

define(['core/context', 'processing/imageLoad'], function(Context, ImageLoadController){

    function getContext(){
        return Context;
    }

    function initProcessingControllers(){
        ImageLoadController.init();
    }

    return{
        getContext:                     getContext,
        initProcessingControllers:      initProcessingControllers
    }
});