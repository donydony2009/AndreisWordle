import random
import enchant
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Word, Guess
from .forms import GuessForm

import random
import enchant
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Word, Guess
from .forms import GuessForm

def get_guess_info(guess, word):
    guess_info = []
    word_remaining = list(word)  # To handle multiple occurrences correctly

    # First pass: check for correct positions
    for idx, letter in enumerate(guess):
        if word[idx] == letter:
            guess_info.append((letter, True, True))
            word_remaining[idx] = None  # Remove the letter from remaining

    # Second pass: check for correct letters in the wrong positions
    for idx, letter in enumerate(guess):
        if (letter, True, True) not in guess_info:
            if letter in word_remaining:
                guess_info.append((letter, True, False))
                word_remaining[word_remaining.index(letter)] = None
            else:
                guess_info.append((letter, False, False))

    return guess_info

def game_view(request):
    try:
        active_word = Word.objects.get(is_active=True)
    except Word.DoesNotExist:
        return HttpResponse("No active word found. Please add a word in the admin interface.")

    dictionary = enchant.Dict("en_US")  # Use English dictionary

    if request.method == 'POST':
        form = GuessForm(request.POST)
        if form.is_valid():
            guess_word = form.cleaned_data['guess'].upper()  # Convert guess to uppercase for consistency
            attempts = Guess.objects.filter(word=active_word, user=request.user).count() + 1

            # Check if guess is a valid English word
            is_valid_word = dictionary.check(guess_word)

            # If word is not valid, render game.html with error message
            if not is_valid_word:
                guesses = Guess.objects.filter(word=active_word, user=request.user)
                return render(request, 'wordle_game/game.html', {
                    'form': form,
                    'guesses': guesses,
                    'max_attempts': 6,
                    'invalid_word_message': f'The word "{guess_word}" is not a valid English word. Please try again.',
                })

            # Generate guess_info for display
            guess_info = get_guess_info(guess_word, active_word.word)

            is_correct = (guess_word == active_word.word)

            Guess.objects.create(
                user=request.user,
                word=active_word,
                guess=guess_word,
                attempts=attempts,
                is_correct=is_correct,
                guess_info=guess_info  # Ensure guess_info is stored correctly
            )

            guesses = Guess.objects.filter(word=active_word, user=request.user)

            game_over = is_correct or attempts >= 6

            return render(request, 'wordle_game/game.html', {
                'form': form,
                'guesses': guesses,
                'max_attempts': 6,
                'guess_info': guess_info,  # Pass guess_info to the template
                'game_over': game_over,
                'active_word': active_word.word if game_over else None
            })

    else:
        form = GuessForm()

    guesses = Guess.objects.filter(word=active_word, user=request.user)

    return render(request, 'wordle_game/game.html', {
        'form': form,
        'guesses': guesses,
        'max_attempts': 6,
    })



def restart_game(request):
    # Deactivate the current active word
    try:
        active_word = Word.objects.get(is_active=True)
        active_word.is_active = False
        active_word.save()
    except Word.DoesNotExist:
        pass

    # Select a random word from the list of words and activate it
    all_words = Word.objects.all()
    new_active_word = random.choice(all_words)
    new_active_word.is_active = True
    new_active_word.save()

    # Clear all guesses related to the current user
    Guess.objects.filter(user=request.user).delete()

    return redirect('game')
