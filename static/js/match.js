document.addEventListener('DOMContentLoaded', () => {
    const wordsContainer = document.getElementById('words_container');
    const translationsContainer = document.getElementById('translations_container');

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

        if (selectedWord && selectedTranslation) {
            if (selectedWord.dataset.id === selectedTranslation.dataset.id) {
                selectedWord.classList.add('matched');
                selectedTranslation.classList.add('matched');
                setTimeout(() => {
                    selectedWord.style.visibility = 'hidden';
                    selectedTranslation.style.visibility = 'hidden';
                    selectedWord = null;
                    selectedTranslation = null;

                    checkCompletion();
                }, 500);
            } else {
                setTimeout(() => {
                    selectedWord.classList.remove('selected');
                    selectedTranslation.classList.remove('selected');
                    selectedWord = null;
                    selectedTranslation = null;
                }, 500);
            }
        }
    }


    function checkCompletion() {
        if (Array.from(wordsContainer.children).every(card => card.style.visibility === 'hidden') &&
            Array.from(translationsContainer.children).every(card => card.style.visibility === 'hidden')) {
            showCompletionModal();
        }
    }

    function showCompletionModal() {
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
            window.location.href = '/';
        });
    }

    function shuffleArray(array) {
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
