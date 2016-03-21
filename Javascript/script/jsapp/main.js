/**
 * Created by JoaoCosta on 20/03/16.
 */

define(['app/runtime'], function(runtime){

    function loadImageByBlob(blob)
    {
        if(blob)
        {
            var imageLoadController = runtime.getManager().getContext().getImageLoadController();
            imageLoadController.loadImageByBlob(blob);
            return true;
        }
        return false;
    }

    function loadImage(imgBase64)
    {
        if(imgBase64)
        {
            var imageLoadController = runtime.getManager().getContext().getImageLoadController();
            imageLoadController.loadImage(imgBase64);
            return true;
        }
        return false;
    }

    return{
        loadImageByBlob:    loadImageByBlob,
        loadImage:          loadImage
    }

});