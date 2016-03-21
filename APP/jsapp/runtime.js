/**
 * Created by JoaoCosta on 20/03/16.
 */

define(['core/manager'], function(Manager){

    function getManager(){
        return Manager;
    }

    function loadImage(evt){

        console.log("estou no runtime");

        Manager.initProcessingControllers();

        var files = evt.target.files; // FileList object
        var fileExtension;

        //it has an extension
        if(files[0].name.lastIndexOf(".") > 0)
        {
            //get the type/text of the file extension
            fileExtension = files[0].name.substring(files[0].name.lastIndexOf(".") + 1, files[0].name.length);
        }

        if (fileExtension === "jpeg" || fileExtension === "jpg"
            || fileExtension === "gif" || fileExtension === "png")
        {
            var imageLoadController = Manager.getContext().getImageLoadController();
            imageLoadController.loadImageByBlob(files[0]);
        }
        else
        {
            alert("Invalid image type, use: jpeg, png, gif");
        }
    }

    if(document.getElementById('Load'))
    {
        document.getElementById('Load').addEventListener('change', loadImage, false);
    }

    return{
        getManager:     getManager
    }

});

