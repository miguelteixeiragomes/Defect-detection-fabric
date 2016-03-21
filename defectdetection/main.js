/**
 * Created by JoaoCosta on 20/03/16.
 */

//teste

define(['app/runtime'], function(runtime){

    function loadImageByBlob(blob)
    {
        if(blob)
        {
            imageLoadController = runtime.getManager().getContext().getImageLoadController();
            imageLoadController.loadImageByBlob(blob);
            return true;
        }
        return false;
    }

    function loadImage(imgBase64)
    {
        if(imgBase64)
        {
            imageLoadController = runtime.getManager().getContext().getImageLoadController();
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