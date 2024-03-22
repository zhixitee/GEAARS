document.addEventListener('DOMContentLoaded', function () {
    let allStars = document.querySelectorAll('.star');
    allStars.forEach(function(star) {
        star.addEventListener('click', function(ev) {
            let span = ev.currentTarget;
            let allStarsInGroup = span.parentNode.querySelectorAll('.star');
            let match = false;
            let num = 0;
            allStarsInGroup.forEach(function(star, index) {
                if (match) {
                    star.classList.remove('rated');
                } else {
                    star.classList.add('rated');
                }
                if (star === span) {
                    match = true;
                    num = index + 1;
                }
            });
            let rating = parseInt(num);
            let ratingInput = span.parentNode.nextElementSibling; 
            ratingInput.value = rating; 
        });
    });
});
