
document.addEventListener('DOMContentLoaded', function () {
    let confettiRunning = false;

    function safeInitConfetti(canvas) {
        if (!confettiRunning) {
            confettiRunning = true;
            initConfetti(canvas);
            setTimeout(() => confettiRunning = false, 5000); // prevent re-triggering
        }
    }

    function toggleImage(elementId) {
        var element = document.getElementById(elementId);
        if (element.style.display === 'none' || !element.style.display) {
            var allImages = document.querySelectorAll('.overlay');
            allImages.forEach(function(image) {
                image.style.display = 'none';
            });
            element.style.display = 'flex';
        } else {
            element.style.display = 'none';
        }
    }


    document.addEventListener('keydown', function (event) {
        switch (event.key) {
            case 'm': // 'm' => meeting record
                toggleImage('meetingRecord');
                safeInitConfetti(document.getElementById("mrCanvas"));
                break;
            case 'o': // 'o' => olympic standard
                toggleImage('worldRecord');
                safeInitConfetti(document.getElementById("wrCanvas"));
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
