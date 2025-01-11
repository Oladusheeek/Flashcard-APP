document.addEventListener('DOMContentLoaded', () => {
    const wordsetContainer = document.getElementById('words');
    const numCardsInput = document.getElementById('num_cards');

    if (!wordsetContainer) {
        console.error("Container with ID 'words' not found!");
        return;
    }

    // Обработка изменения количества карточек
    numCardsInput.addEventListener('change', () => {
        const currentNumCards = wordsetContainer.children.length;
        const newNumCards = parseInt(numCardsInput.value);

        if (newNumCards > currentNumCards) {
            for (let i = currentNumCards; i < newNumCards; i++) {
                const newCard = document.createElement('div');
                newCard.className = 'word_container';
                newCard.innerHTML = `
                    <label>${i + 1}.</label>
                    <input type="text" class="input_word" name="word" placeholder="word" required>
                    <input type="text" class="input_transcription" name="transcription" placeholder="transcription">
                    <input type="text" class="input_translation" name="translation" placeholder="translation">
                    <input type="text" class="input_description" name="description" placeholder="description">
                `;
                wordsetContainer.appendChild(newCard);
            }
        } else if (newNumCards < currentNumCards) {
            for (let i = currentNumCards; i > newNumCards; i--) {
                wordsetContainer.removeChild(wordsetContainer.lastChild);
            }
        }
    });

    // Обработка удаления карточки
    wordsetContainer.addEventListener('click', (event) => {
        if (event.target.classList.contains('delete_btn')) {
            const wordId = event.target.getAttribute('data-word-id');
            if (!wordId) {
                console.error("Word ID not found!");
                return;
            }
            console.log(`Delete button clicked for word ID: ${wordId}`);

            // Отправляем запрос на сервер для удаления карточки
            fetch(`/delete_word/${wordId}`, {
                method: 'DELETE',
            })
            .then(response => {
                if (response.ok) {
                    console.log(`Word ID ${wordId} deleted successfully`);
                    event.target.closest('.word_container').remove();

                    // Обновляем количество карточек
                    const remainingCards = wordsetContainer.children.length;
                    numCardsInput.value = remainingCards;
                } else {
                    return response.text().then(text => { throw new Error(text) });
                }
            })
            .catch(error => {
                console.error('Error: ', error.message);
            });
        }
    });
});
