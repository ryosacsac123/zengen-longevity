
document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-btn');
    const landingContent = document.getElementById('landing-content');
    const diagnosticForm = document.getElementById('diagnostic-form');
    const resultsView = document.getElementById('results-view');
    const auditForm = document.getElementById('audit-form');
    const restartBtn = document.getElementById('restart-btn');

    startBtn.addEventListener('click', () => {
        // 1. Trigger Physics Effect
        if (typeof triggerGravitySuck === 'function') {
            triggerGravitySuck();
        }

        // 2. Hide Landing, Show Form
        landingContent.style.opacity = '0';
        setTimeout(() => {
            landingContent.classList.add('hidden');
            diagnosticForm.classList.remove('hidden');
            // Small delay to allow CSS display:block to apply before opacity transition
            setTimeout(() => {
                diagnosticForm.style.opacity = '1';
            }, 10);
        }, 500);
    });

    auditForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Harvest data
        const formData = new FormData(auditForm);
        const data = {};

        // List of all expected keys
        const keys = ['rice', 'miso_soup', 'seaweed', 'pickles', 'green_yellow_veg', 'fish', 'green_tea', 'beef_pork'];

        keys.forEach(key => {
            // Checkbox: on = true, missing = false
            data[key] = formData.has(key);
        });

        console.log("Sending data:", data);

        try {
            const response = await fetch('/api/calculate_score', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            // Show Results
            diagnosticForm.style.opacity = '0';
            setTimeout(() => {
                diagnosticForm.classList.add('hidden');
                resultsView.classList.remove('hidden');
                window.scrollTo({ top: 0, behavior: 'smooth' }); // Fix: Scroll to top prevents cutoff

                document.getElementById('score-display').textContent = `${result.score} / 8`;
                document.getElementById('risk-reduction').textContent = `Risk Reduction: ${result.risk_reduction}`;

                const breakdownHtml = result.details.map(d => `<p>${d}</p>`).join('');
                document.getElementById('breakdown').innerHTML = breakdownHtml;

                setTimeout(() => {
                    resultsView.style.opacity = '1';
                }, 10);
            }, 500);

        } catch (error) {
            console.error('Error:', error);
            alert('Failed to calculate score. Check console.');
        }
    });

    restartBtn.addEventListener('click', () => {
        location.reload();
    });

    const buyBtn = document.getElementById('buy-btn');
    if (buyBtn) {
        buyBtn.addEventListener('click', () => {
            fetch('/create-checkout-session', {
                method: 'POST',
            })
                .then(function (response) {
                    return response.json();
                })
                .then(function (session) {
                    if (session.error) {
                        alert(session.error);
                    } else {
                        const stripe = Stripe(STRIPE_PUBLISHABLE_KEY);
                        return stripe.redirectToCheckout({ sessionId: session.id });
                    }
                })
                .then(function (result) {
                    if (result.error) {
                        alert(result.error.message);
                    }
                })
                .catch(function (error) {
                    console.error('Error:', error);
                });
        });
    }
});
