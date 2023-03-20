$(document).ready(function() {
    const dataUrl = sessionStorage.getItem('recipeImage');
    if (dataUrl) {
        const $img = $('<img>').attr('src', dataUrl);
        $('.drag-area').html($img);
    }
});
