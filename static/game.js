$(function () {
    // Initialize autocomplete with suggestions
    $("#input_text").autocomplete({
        source: function (request, response) {
            $.ajax({
                type: "POST",
                url: window.URLS.get_suggestions,
                dataType: "json",
                cache: false,
                data: {
                    q: request.term
                },
                success: function (data) {
                    console.log('Suggestions received:', data);
                    response(data);
                },
                error: function (jqXHR, textStatus, errorThrown) {
                    console.log('Autocomplete error:', textStatus, errorThrown);
                }
            });
        },
        minLength: 1,
        select: function (event, ui) {
            // Auto-submit when user selects from dropdown
            setTimeout(function () {
                $('#guess-form').submit();
            }, 50);
        }
    });

    // AJAX form submission for guesses
    $('#guess-form').on('submit', function (e) {
        e.preventDefault();

        const guessValue = $('#input_text').val().trim();
        if (!guessValue) {
            // showMessage('Please enter a card name', 'error');
            return;
        }

        // Disable the form while processing
        $('#guess-form button').prop('disabled', true);

        $.ajax({
            type: 'POST',
            url: window.URLS.submit_guess,
            data: { guess: guessValue },
            dataType: 'json',
            success: function (response) {
                if (response.success) {
                    addRowToTable(response.row);
                    $('#input_text').val(''); // Clear input

                    if (response.finished) {
                        $('#congratulations').text(response.message).show();
                    }
                } else {
                    showMessage('Error: ' + response.error, 'error');
                }
            },
            error: function () {
                showMessage('Error submitting guess. Please try again.', 'error');
            },
            complete: function () {
                // Re-enable the form
                $('#guess-form button').prop('disabled', false);
                $('#input_text').focus();
            }
        });
    });

    // AJAX reset functionality
    $('#reset-form').on('submit', function (e) {
        e.preventDefault();

        // Disable the reset button while processing
        $('#reset-form button').prop('disabled', true);

        $.ajax({
            type: 'POST',
            url: window.URLS.reset_game,
            dataType: 'json',
            success: function (response) {
                if (response.success) {
                    // Clear the table and congratulations message
                    $('#game-table tbody').empty();
                    $('#congratulations').hide();
                    $('#input_text').val('').focus();
                    showMessage('New game started!', 'success');
                } else {
                    showMessage('Error resetting game. Please try again.', 'error');
                }
            },
            error: function () {
                showMessage('Error resetting game. Please try again.', 'error');
            },
            complete: function () {
                // Re-enable the reset button
                $('#reset-form button').prop('disabled', false);
            }
        });
    });

    // Function to add a new row to the table
    function addRowToTable(rowData) {
        let rowHtml = '<tr>';

        rowData.forEach(function (cellData, index) {
            const [value, color] = cellData;

            if (index === 0) { // Card image
                rowHtml += `<td class="${color}"><img src="${value[1]}" height="150" width="100" alt="Card image"></td>`;
            } else { // Other columns with arrows
                const [upArrow, cellValue, downArrow] = value;
                rowHtml += `<td class="${color}">
                    <div class="${upArrow}">▲</div>
                    <div class="white-text">${cellValue}</div>
                    <div class="${downArrow}">▼</div>
                </td>`;
            }
        });

        rowHtml += '</tr>';
        const $newRow = $(rowHtml).addClass('new-row');
        $('#game-table tbody').append($newRow);

        // Scroll the new row into view
        $newRow[0].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    // Function to show temporary messages
    function showMessage(message, type) {
        // Remove any existing message
        $('.temp-message').remove();

        const messageClass = type === 'error' ? 'alert-error' : 'alert-success';
        const $message = $(`<div class="temp-message ${messageClass}">${message}</div>`);

        // Add styles
        $message.css({
            'position': 'fixed',
            'top': '20px',
            'right': '20px',
            'padding': '12px 20px',
            'border-radius': '6px',
            'color': 'white',
            'font-weight': 'bold',
            'z-index': '9999',
            'animation': 'slideInRight 0.3s ease-out',
            'background-color': type === 'error' ? '#dc3545' : '#28a745'
        });

        $('body').append($message);

        // Auto-remove after 3 seconds
        setTimeout(function () {
            $message.fadeOut(300, function () {
                $(this).remove();
            });
        }, 3000);
    }

    // Focus on input field when page loads
    $('#input_text').focus();

    // Add keyboard shortcut for reset (Ctrl/Cmd + R)
    $(document).on('keydown', function (e) {
        if ((e.ctrlKey || e.metaKey) && e.keyCode === 82) {
            e.preventDefault();
            $('#reset-form').submit();
        }
    });
}); 