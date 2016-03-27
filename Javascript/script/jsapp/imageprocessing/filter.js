/**
 * Created by JoaoCosta on 27/03/16.
 */

define(['base64', 'core/context'], function(Base64, Context) {

    function applyBlackAndWhite()
    {
        var imageLoadController = Context.getImageLoadController();
        var image = imageLoadController.loadedImage;
        if(!image)
        {
            throw new Error("No image loaded");
            return false;
        }
        console.log(image.src);
        return true;
    }

    function init()
    {
        Context.setFiltersController(this);
    }

    return{
        init:                       init,
        applyBlackAndWhite:         applyBlackAndWhite
    }
});
