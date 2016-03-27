/**
 * Created by JoaoCosta on 20/03/16.
 */

define(['base64', 'app/runtime', 'core/context', 'processing/filter'],
    function(Base64, Runtime, Context, Filter) {

        var loadedImage = new Image();

        /**
         * This function is a promise that reads an image file
         * @param file image file
         * @param fileReader file reader
         * @returns Promise The image base64
         */
        function readImageBlobPromise(file, fileReader)
        {
            return new Promise(function(resolve,reject) {
                fileReader.onload = function() {
                    resolve(fileReader.result);
                };
                fileReader.onerror = function() {
                    reject(fileReader.error);
                };
                fileReader.readAsDataURL(file);
            })
        }

        function loadImageByBlob(file)
        {
            var reader = new FileReader();
            // Wait for file to be read
            readImageBlobPromise(file, reader).then(function(base64Data){
                loadImage(base64Data);
            }).catch(function(error){
                throw new Error("Could not load image from blob");
            });
        }

        function loadImage(imgSource, extension)
        {
            // Prepare data for creation of image object
            var imgBase64;
            if (!extension)
            {
                imgBase64 = imgSource;
                imgSource = imgBase64.split(',')[1];
                extension = imgBase64.substring(imgBase64.indexOf("/")+1, imgBase64.indexOf(";"));
            }
            else
            {
                imgBase64 = "data:image/" + extension + ";base64," + imgSource;
            }

            loadedImage.src = imgBase64;
            
            Filter.init();
            
        }

        function init()
        {
            Context.setImageLoadController(this);
        }

        return{
            loadedImage:            loadedImage,
            init:                   init,
            loadImageByBlob:        loadImageByBlob,
            loadImage:              loadImage
        }
});
