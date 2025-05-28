
function initConfetti(canvas) {
  const ctx = canvas.getContext("2d");
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
  const cx = canvas.width / 2;
  const cy = canvas.height / 2;

  const parentDiv = canvas.parentElement; 

  let confetti = [];
  const confettiCount = 200;
  const gravity = 0.5;
  const terminalVelocity = 5;
  const drag = 0.075;
  const colors = [
      { front: 'red', back: 'darkred' },
      { front: 'green', back: 'darkgreen' },
      { front: 'blue', back: 'darkblue' },
      { front: 'yellow', back: 'darkyellow' },
      { front: 'orange', back: 'darkorange' },
      { front: 'pink', back: 'darkpink' },
      { front: 'purple', back: 'darkpurple' },
      { front: 'turquoise', back: 'darkturquoise' }];

  function randomRange(min, max) {
      return Math.random() * (max - min) + min;
  }

  let animationFrameId = null;

  function stopConfetti() {
      if (animationFrameId) {
          cancelAnimationFrame(animationFrameId);
          animationFrameId = null;
      }
  }

  function render() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      confetti.forEach((confetto, index) => {
          let width = confetto.dimensions.x * confetto.scale.x;
          let height = confetto.dimensions.y * confetto.scale.y;

          ctx.translate(confetto.position.x, confetto.position.y);
          ctx.rotate(confetto.rotation);

          confetto.velocity.x -= confetto.velocity.x * drag;
          confetto.velocity.y = Math.min(confetto.velocity.y + gravity, terminalVelocity);
          confetto.velocity.x += Math.random() > 0.5 ? Math.random() : -Math.random();

          confetto.position.x += confetto.velocity.x;
          confetto.position.y += confetto.velocity.y;

          if (confetto.position.y >= canvas.height) confetti.splice(index, 1);

          if (confetto.position.x > canvas.width) confetto.position.x = 0;
          if (confetto.position.x < 0) confetto.position.x = canvas.width;

          confetto.scale.y = Math.cos(confetto.position.y * 0.1);
          ctx.fillStyle = confetto.scale.y > 0 ? confetto.color.front : confetto.color.back;

          ctx.fillRect(-width / 2, -height / 2, width, height);
          ctx.setTransform(1, 0, 0, 1, 0, 0);
      });

      animationFrameId = window.requestAnimationFrame(render);
  }

  stopConfetti(); // Stop any previous animation loop

  for (let i = 0; i < confettiCount; i++) {
      confetti.push({
          color: colors[Math.floor(randomRange(0, colors.length))],
          dimensions: {
              x: randomRange(10, 20),
              y: randomRange(10, 30)
          },
          position: {
              x: randomRange(0, canvas.width),
              y: canvas.height - 1
          },
          rotation: randomRange(0, 2 * Math.PI),
          scale: {
              x: 1,
              y: 1
          },
          velocity: {
              x: randomRange(-25, 25),
              y: randomRange(0, -50)
          }
      });
  }

  render();
}

initConfetti(document.getElementById("mrCanvas"));
initConfetti(document.getElementById("wrCanvas"));
