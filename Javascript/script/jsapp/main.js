/**
 * Created by JoaoCosta on 20/03/16.
 */
require(['app/runtime'], function(Runtime){

    function ImageProcessingAPI(){
        function loadImageByBlob(blob)
        {
            if(blob)
            {
                var manager = Runtime.getManager();
                manager.initProcessingControllers();
                var imageLoadController = manager.getContext().getImageLoadController();
                imageLoadController.loadImageByBlob(blob);
                return true;
            }
        }

        function loadImage(imgBase64, extension)
        {
            if(imgBase64)
            {
                var manager = Runtime.getManager();
                manager.initProcessingControllers();
                var imageLoadController = manager.getContext().getImageLoadController();
                imageLoadController.loadImage(imgBase64, extension);
                return true;
            }
        }

        function blackAndWhite()
        {
            var filtersController = Runtime.getManager().getContext().getFiltersController();
            return filtersController.applyBlackAndWhite();
        }


        return{
            loadImageByBlob:    loadImageByBlob,
            loadImage:          loadImage,
            blackAndWhite:      blackAndWhite
        };
    }

    var ImageProcessor = {};
    ImageProcessor.API = function(){
        window.ImageProcessingAPI = ImageProcessingAPI();
    };
    ImageProcessor.API();

});