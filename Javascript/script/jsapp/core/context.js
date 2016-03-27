/**
 * Created by Joao Costa on 20/03/16.
 */

define(function(){
    "use strict";

    var imageLoadController;
    var filtersController;

    function setImageLoadController(ref)
    {
        imageLoadController = ref;
    }

    function setFiltersController(ref)
    {
        filtersController = ref;
    }

    function getImageLoadController()
    {
        return imageLoadController;
    }

    function getFiltersController()
    {
        return filtersController;
    }

    return{
        setImageLoadController:     setImageLoadController,
        setFiltersController:       setFiltersController,
        getImageLoadController:     getImageLoadController,
        getFiltersController:       getFiltersController
    }
});