<<<<<<< HEAD
$(document).ready(function() {
    const dataUrl = sessionStorage.getItem('recipeImage');
    if (dataUrl) {
        const $img = $('<img>').attr('src', dataUrl);
        $('.drag-area').html($img);
    }
});
=======
$(document).ready(function() {
    const dataUrl = sessionStorage.getItem('recipeImage');
    if (dataUrl) {
        const $img = $('<img>').attr('src', dataUrl);
        $('.drag-area').html($img);
    }
});
>>>>>>> d981ace22a14f827a0360947269308e48e916a69
