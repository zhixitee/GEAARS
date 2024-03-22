document.addEventListener('DOMContentLoaded', function () {
    let allStars = document.querySelectorAll('.star');
    let ratingSystem = document.querySelector('.rating-system');
    let userHasSubmittedReview = ratingSystem.dataset.userHasSubmittedReview === 'True';

    if (userHasSubmittedReview) {
        disableRating();
    }
    // Function to handle star click events
    function handleStarClick(ev) {
        let span = ev.currentTarget;
        
        if (span.parentNode.classList.contains('disabled')) {
            return; // Do nothing if the rating system is disabled
        }

        let userHasSubmittedReview = ratingSystem.dataset.userHasSubmittedReview === 'True';
        if (userHasSubmittedReview) {
        disableRating();
        }
        
        let allStarsInGroup = span.parentNode.querySelectorAll('.star');
        let clickedIndex = Array.from(allStarsInGroup).indexOf(span); // Find the index of the clicked star
    
        allStarsInGroup.forEach(function(star, index) {
            if (index <= clickedIndex) {
                star.classList.add('rated'); // Add 'rated' class up to and including the clicked star
            } else {
                star.classList.remove('rated'); // Remove 'rated' class for stars after the clicked one
            }
        });
    
        let rating = clickedIndex + 1; // Update the rating based on clicked star index
        let ratingInput = span.parentNode.nextElementSibling; // Find the corresponding input to update
        if (ratingInput) {
            ratingInput.value = rating; // Update the input's value to the selected rating
        }
    }
    
    // Attach the event listener to stars as before
    document.querySelectorAll('.star').forEach(function(star) {
        star.addEventListener('click', handleStarClick);
    });

    function disableRating() {
        let ratingSystems = document.querySelectorAll('.rating-system');
        ratingSystems.forEach(function(system) {
            system.classList.add('disabled');
        });

        // Remove the event listeners from stars to make them non-clickable
        allStars.forEach(function(star) {
            star.removeEventListener('click', handleStarClick);
        });
    }


    // Disable the rating system upon form submission
    let form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function(event) {
            disableRating();
        });
    }


    
});