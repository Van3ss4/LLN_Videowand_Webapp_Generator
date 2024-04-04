import {initConfetti} from './confettiEffect.js';


document.addEventListener('DOMContentLoaded', function() {
    // Define a reusable function to toggle image visibility
    function toggleImage(elementId) {
        var element = document.getElementById(elementId);
        if (element.style.display === 'none') {
            // Close all other images
            var allImages = document.querySelectorAll('.overlay');
            allImages.forEach(function(image) {
                image.style.display = 'none';
            });
            // Open the selected image
            element.style.display = 'flex';
        } else {
            element.style.display = 'none';
        }
    }

    // Define keyboard shortcuts for different images
    document.addEventListener('keydown', function(event) {
        switch (event.key) {
            case 'm': // 'm' => meeting record
                toggleImage('meetingRecord');
                initConfetti(document.getElementById("mrCanvas"));
                break;
            case 'w': // 'w' => world record
                toggleImage('worldRecord');
                initConfetti(document.getElementById("wrCanvas"));
                break;
            case 's': // 's' => all sponsors
                toggleImage('allSponsors');
                break;
            case 'l': // 'l' => lgr
                toggleImage('lgr');
                break;
            case 'p': // 'p' => pacersInAllRaces
                toggleImage('pacersInAllRaces');
                break;
            default:
                break;
        }
    });
});
