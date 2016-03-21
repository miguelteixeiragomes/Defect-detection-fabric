/**
 * Created by JoaoCosta on 20/03/16.
 */

define(['base64'], function(Base64) {

    function loadImageByBlob(blob)
    {
        console.log("test");
    }

    function init()
    {
        Context.setImageProcessingController(this);
    }

    return{
        init:               init,
        loadImageByBlob:    loadImageByBlob
    }
});
