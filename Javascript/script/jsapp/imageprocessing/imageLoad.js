/**
 * Created by JoaoCosta on 20/03/16.
 */

define(['base64', 'core/context'], function(Base64, Context) {

    function loadImageByBlob(blob)
    {
        console.log("test");
    }

    function init()
    {
        Context.setImageLoadController(this);
    }

    return{
        init:               init,
        loadImageByBlob:    loadImageByBlob
    }
});
