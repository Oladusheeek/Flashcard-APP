document.addEventListener('DOMContentLoaded', () => {
    const saveButton = document.getElementById('save-button');
    const numCardsInput = document.getElementById('num_cards');
    const wordsetContainer = document.getElementById('words');

    // Сохранение изменений
    saveButton.addEventListener('click', () => {
        const formData = new FormData(document.getElementById('edit_wordset_form'));

        fetch(window.location.pathname, {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (response.ok) {
                console.log('Changes saved successfully!');
                window.location.href = '/'; // Redirect to home page
            } else {
                return response.text().then(text => { throw new Error(text) });
            }
        })
        .catch(error => {
            alert('Error: ' + error.message);
        });
    });

    // Обновление количества карточек
    numCardsInput.addEventListener('change', (event) => {
        const currentNumCards = wordsetContainer.children.length;
        const newNumCards = parseInt(event.target.value);

        if (newNumCards > currentNumCards) {
            for (let i = currentNumCards; i < newNumCards; i++) {
                const newCard = document.createElement('div');
                newCard.className = 'word_container';
                newCard.innerHTML = `
                    <label>${i + 1}.</label>
                    <input type="hidden" name="new_word_id_${i}" value="new_${i}">
                    <input type="text" class="input_word" name="new_word_${i}" placeholder="word" required>
                    <input type="text" class="input_transcription" name="new_transcription_${i}" placeholder="transcription">
                    <input type="text" class="input_translation" name="new_translation_${i}" placeholder="translation">
                    <input type="text" class="input_description" name="new_description_${i}" placeholder="description">
                `;
                wordsetContainer.appendChild(newCard);
            }
        } else if (newNumCards < currentNumCards) {
            for (let i = currentNumCards; i > newNumCards; i--) {
                wordsetContainer.removeChild(wordsetContainer.lastChild);
            }
        }
    });

    // Удаление карточки
    wordsetContainer.addEventListener('click', (event) => {
        if (event.target.classList.contains('delete_b')) {
            const wordId = event.target.getAttribute('data-word-id');
            console.log(`Delete button clicked for word ID: ${wordId}`); // Для отладки

            // Отправляем запрос на сервер для удаления карточки
            fetch(`/delete_word/${wordId}`, {
                method: 'DELETE',
            })
            .then(response => {
                if (response.ok) {
                    // Удаляем карточку из DOM
                    console.log(`Word ID ${wordId} deleted successfully`); // Для отладки
                    event.target.closest('.word_container').remove();
                } else {
                    return response.text().then(text => { throw new Error(text) });
                }
            })
            .catch(error => {
                alert('Error: ' + error.message);
            });
        }
    });
});
