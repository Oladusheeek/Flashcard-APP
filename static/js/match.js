document.addEventListener('DOMContentLoaded', () => {
    const wordsContainer = document.getElementById('words_container');
    const translationsContainer = document.getElementById('translations_container');

    // Random sorting of cards
    const shuffledWords = shuffleArray(Array.from(wordsContainer.children));
    const shuffledTranslations = shuffleArray(Array.from(translationsContainer.children));

    wordsContainer.innerHTML = '';
    translationsContainer.innerHTML = '';

    shuffledWords.forEach(word => wordsContainer.appendChild(word));
    shuffledTranslations.forEach(translation => translationsContainer.appendChild(translation));

    let selectedWord = null;
    let selectedTranslation = null;

    function onCardClick(event) {
        const card = event.target;
        const id = card.dataset.id;
        const type = card.dataset.type;

        if (type === 'word') {
            if (selectedWord) {
                selectedWord.classList.remove('selected');
            }
            selectedWord = card;
        } else {
            if (selectedTranslation) {
                selectedTranslation.classList.remove('selected');
            }
            selectedTranslation = card;
        }

        card.classList.add('selected');
        // if word and translation from one card then..
        if (selectedWord && selectedTranslation) {
            if (selectedWord.dataset.id === selectedTranslation.dataset.id) {
                selectedWord.classList.add('matched');
                selectedTranslation.classList.add('matched');
                setTimeout(() => { //.. word and translation now hidden..
                    selectedWord.style.visibility = 'hidden';
                    selectedTranslation.style.visibility = 'hidden';
                    //.. and selection in no longer selected
                    selectedWord = null;
                    selectedTranslation = null;

                    checkCompletion(); //after each pair of correctly matched words there is a check for completion of test
                }, 500);
            } else {
                setTimeout(() => {
                    //If selected words are no match then selection is removed from both 'word' and 'translation'
                    selectedWord.classList.remove('selected');
                    selectedTranslation.classList.remove('selected');
                    selectedWord = null;
                    selectedTranslation = null;
                }, 500);
            }
        }
    }


    function checkCompletion() { //if all elements are now hidden then test was completed
        if (Array.from(wordsContainer.children).every(card => card.style.visibility === 'hidden') &&
            Array.from(translationsContainer.children).every(card => card.style.visibility === 'hidden')) {
            showCompletionModal();
        }
    }

    function showCompletionModal() { // Congratulation notification
        const modal = document.createElement('div');
        modal.className = 'modal';
        modal.innerHTML = `
            <div class="modal-content">
                <h2 class="modal_title">Good job!!!</h2>
                <h2 class="modal_title">You passed mathcing test!<h2>
                <button class="btn_closeModal" id="closeModal">Back</button>
            </div>
        `;
        document.body.appendChild(modal);

        document.getElementById('closeModal').addEventListener('click', () => {
            window.location.href = '/'; //back to main screen
        });
    }

    function shuffleArray(array) { //randomizer of cards
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]];
        }
        return array;
    }

    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('click', onCardClick);
    });
});
