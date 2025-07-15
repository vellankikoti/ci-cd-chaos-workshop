#!/usr/bin/env python3
"""
Docker Escape Room Challenge - Web UI
A gamified Docker learning experience
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import subprocess
import json
import random
import time
import os
import re
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'docker-escape-room-secret-key-2025'

# Game configuration
PUZZLES = {
    1: {
        'name': 'The Secret Vault',
        'clue': 'Dr. Bug has hidden the Escape Key inside a secret volume. Find the secret code in vault-volume at /secret/code.txt',
        'answer': 'escape123',
        'points': 10,
        'docker_command': 'docker run --rm -v vault-volume:/mnt busybox cat /mnt/secret/code.txt',
        'setup_script': 'puzzles/puzzle1_volume.sh',
        'hint': 'Use docker run with volume mounting to access files inside a volume',
        'type': 'exact',
    },
    2: {
        'name': 'The Network Detective',
        'clue': 'Dr. Bug has created a mysterious container. Find the IP address of the container named "network-spy" and submit it.',
        'answer': r'^(172\.\d+\.\d+\.\d+)$',
        'points': 10,
        'docker_command': 'docker inspect network-spy | grep IPAddress',
        'setup_script': 'puzzles/puzzle2_network.sh',
        'hint': 'Use docker inspect to get detailed information about a container',
        'type': 'regex',
    },
    3: {
        'name': 'The Memory Detective',
        'clue': 'A container keeps crashing! Find the exact memory limit (in MB) of the container named "memory-victim" and submit it.',
        'answer': r'^(10|10485760)$',
        'points': 10,
        'docker_command': 'docker inspect memory-victim | grep -i memory',
        'setup_script': 'puzzles/puzzle3_memory.sh',
        'hint': 'Use docker inspect to examine container configuration and resource limits',
        'type': 'regex',
    },
    4: {
        'name': 'The Secret Hunter',
        'clue': 'Dr. Bug has hidden a secret environment variable. Find the value of SECRET_CODE in container "secret-keeper" and submit it.',
        'answer': 'docker_master_2025',
        'points': 10,
        'docker_command': 'docker inspect secret-keeper | grep -A 10 -B 5 SECRET_CODE',
        'setup_script': 'puzzles/puzzle4_inspect.sh',
        'hint': 'Use docker inspect to examine environment variables in a container',
        'type': 'exact',
    },
    5: {
        'name': 'The Image Sleuth',
        'clue': 'Dr. Bug has created a suspicious image. Find the exact size (in MB) of the image "suspicious-image" and submit it.',
        'answer': r'^(\d{2,4})$',
        'points': 10,
        'docker_command': 'docker images suspicious-image',
        'setup_script': 'puzzles/puzzle5_multistage/setup.sh',
        'hint': 'Use docker images to list image information including sizes',
        'type': 'regex',
    }
}

# Dr. Bug's taunts
TAUNTS = [
    "🐛 Your pipeline is as stable as my coffee after 3 AM!",
    "🐛 I've seen better error handling in a hello-world app!",
    "🐛 Your containers are more broken than my last deployment!",
    "🐛 Even my pet goldfish knows more about Docker than you!",
    "🐛 Welcome to my chaos laboratory - where bugs become features!",
    "🐛 Your CI/CD pipeline is giving me second-hand embarrassment!",
    "🐛 Maybe stick to `docker ps` and call it a career!",
    "🐛 I create chaos, you create... whatever this is!",
    "🐛 Your debugging skills are as weak as your container security!",
    "🐛 Maybe try reading the documentation next time? Oh wait, you probably can't read!",
    "🐛 Another failure? I'm starting to feel bad for you. Just kidding!",
    "🐛 Are you sure you're a developer? You seem more like a `docker rm` expert!",
    "🐛 Your containers are as broken as your understanding of Docker!",
    "🐛 I've seen better Docker skills in a `hello-world` tutorial!",
    "🐛 Maybe you should stick to `docker ps` and call it a day!",
    "🐛 Your chaos engineering skills are as predictable as a broken CI/CD pipeline!",
    "🐛 I hope you like inspecting things. Because you're going to be stuck inspecting this vault forever!",
    "🐛 Your containers are as stable as my production environment on a Monday morning!",
    "🐛 Another bug in your code? How original!",
    "🐛 Your Docker skills are giving me deployment anxiety!"
]

SUCCESS_MESSAGES = [
    "🐛 Hmph. You're starting to understand my chaos methods...",
    "🐛 Not bad... for someone who probably Googles 'Docker basics' daily!",
    "🐛 You're learning. Slowly. Like my CI/CD pipeline on a Monday morning!",
    "🐛 Well done, but don't get cocky. My chaos is infinite!",
    "🐛 You're starting to impress me. Just a little.",
    "🐛 Well done, but don't get cocky. There's more chaos where that came from!",
    "🐛 You're making progress. Don't let it go to your head.",
    "🐛 I'll give you that one. But the next puzzle will be your downfall!",
    "🐛 You're not completely hopeless. Yet.",
    "🐛 A broken container can still run, I guess.",
    "🐛 You're learning. Slowly. Very slowly."
]

def initialize_game():
    session['current_puzzle'] = 1
    session['score'] = 0
    session['start_time'] = time.time()
    session['attempts'] = 0
    session['completed_puzzles'] = []
    session['game_completed'] = False
    session['hint_used'] = {}
    
    # Auto-setup all puzzles for seamless experience
    setup_all_puzzles()

def setup_all_puzzles():
    """Setup all puzzles automatically for seamless workshop experience"""
    print("🐛 Dr. Bug is setting up his chaos laboratory...")
    for puzzle_id, puzzle in PUZZLES.items():
        try:
            print(f"Setting up Puzzle {puzzle_id}: {puzzle['name']}")
            success = run_setup_script(puzzle['setup_script'])
            if success:
                print(f"✅ Puzzle {puzzle_id} setup successful")
            else:
                print(f"❌ Puzzle {puzzle_id} setup failed")
        except Exception as e:
            print(f"❌ Warning: Could not setup puzzle {puzzle_id}: {e}")
    print("✅ All puzzles are ready for chaos!")

def get_random_taunt():
    return random.choice(TAUNTS)

def get_random_success():
    return random.choice(SUCCESS_MESSAGES)

def run_setup_script(script_path):
    try:
        result = subprocess.run(['bash', script_path], capture_output=True, text=True, timeout=30)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running setup script {script_path}: {e}")
        return False

def check_puzzle_answer(puzzle_id, user_answer):
    puzzle = PUZZLES.get(puzzle_id)
    if not puzzle:
        return False, "Invalid puzzle"
    answer = user_answer.strip().lower()
    if puzzle['type'] == 'exact':
        return answer == str(puzzle['answer']).strip().lower(), "Answer checked"
    elif puzzle['type'] == 'regex':
        # Accept any value that matches the regex (e.g., IP, MB, etc)
        return bool(re.match(puzzle['answer'], answer)), "Answer checked"
    return False, "Unknown puzzle type"

@app.route('/')
def index():
    # Always reset session for a fresh start
    session.clear()
    initialize_game()
    current_puzzle = session.get('current_puzzle', 1)
    puzzle = PUZZLES.get(current_puzzle)
    if not puzzle:
        return redirect(url_for('game_complete'))
    show_command = session.get('hint_used', {}).get(str(current_puzzle), False)
    return render_template('escape.html',
        puzzle=puzzle,
        current_puzzle=current_puzzle,
        score=session.get('score', 0),
        attempts=session.get('attempts', 0),
        total_puzzles=len(PUZZLES),
        show_command=show_command)

@app.route('/get_hint', methods=['POST'])
def get_hint():
    puzzle_id = session.get('current_puzzle', 1)
    puzzle = PUZZLES.get(puzzle_id)
    if puzzle:
        # Mark hint as used for this puzzle
        hint_used = session.get('hint_used', {})
        hint_used[str(puzzle_id)] = True
        session['hint_used'] = hint_used
        return jsonify({
            'hint': puzzle['hint'],
            'command': puzzle['docker_command']
        })
    else:
        return jsonify({'error': 'Puzzle not found'})

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    user_answer = data.get('answer', '').strip()
    puzzle_id = session.get('current_puzzle', 1)
    session['attempts'] = session.get('attempts', 0) + 1
    is_correct, message = check_puzzle_answer(puzzle_id, user_answer)
    if is_correct:
        puzzle = PUZZLES.get(puzzle_id)
        points_earned = puzzle['points']
        session['score'] = session.get('score', 0) + points_earned
        completed = session.get('completed_puzzles', [])
        completed.append(puzzle_id)
        session['completed_puzzles'] = completed
        if puzzle_id < len(PUZZLES):
            session['current_puzzle'] = puzzle_id + 1
            response = {
                'success': True,
                'message': get_random_success(),
                'points_earned': points_earned,
                'new_score': session['score'],
                'next_puzzle': puzzle_id + 1,
                'game_complete': False
            }
        else:
            session['game_completed'] = True
            response = {
                'success': True,
                'message': 'Congratulations! You have escaped the Docker Vault!',
                'points_earned': points_earned,
                'new_score': session['score'],
                'game_complete': True
            }
    else:
        penalty = 3
        session['score'] = max(0, session.get('score', 0) - penalty)
        response = {
            'success': False,
            'message': get_random_taunt(),
            'penalty': penalty,
            'new_score': session['score']
        }
    return jsonify(response)

@app.route('/skip', methods=['POST'])
def skip_puzzle():
    current_puzzle = session.get('current_puzzle', 1)
    if current_puzzle < len(PUZZLES):
        session['current_puzzle'] = current_puzzle + 1
    return jsonify({'ok': True, 'current_puzzle': session['current_puzzle']})

@app.route('/back', methods=['POST'])
def back_puzzle():
    current_puzzle = session.get('current_puzzle', 1)
    if current_puzzle > 1:
        session['current_puzzle'] = current_puzzle - 1
    return jsonify({'ok': True, 'current_puzzle': session['current_puzzle']})

@app.route('/current_puzzle')
def current_puzzle_data():
    current_puzzle = session.get('current_puzzle', 1)
    puzzle = PUZZLES.get(current_puzzle)
    show_command = session.get('hint_used', {}).get(str(current_puzzle), False)
    data = {
        'name': puzzle['name'],
        'clue': puzzle['clue'],
        'hint': puzzle['hint'],
        'show_command': show_command,
        'command': puzzle['docker_command'] if show_command else None,
        'current_puzzle': current_puzzle,
        'score': session.get('score', 0),
        'attempts': session.get('attempts', 0),
        'total_puzzles': len(PUZZLES)
    }
    return jsonify(data)

@app.route('/game_complete')
def game_complete():
    if not session.get('game_completed', False):
        return redirect(url_for('index'))
    end_time = time.time()
    start_time = session.get('start_time', end_time)
    time_taken = end_time - start_time
    return render_template('complete.html',
        score=session.get('score', 0),
        time_taken=time_taken,
        total_puzzles=len(PUZZLES),
        show_restart=True)

@app.route('/reset')
def reset_game():
    session.clear()
    initialize_game()
    return redirect(url_for('index'))

@app.route('/force_setup')
def force_setup():
    """Force re-setup of all puzzles (for debugging)"""
    setup_all_puzzles()
    return jsonify({'status': 'success', 'message': 'All puzzles re-setup!'})

@app.route('/test_setup')
def test_setup():
    """Test endpoint to manually trigger setup"""
    setup_all_puzzles()
    return jsonify({'status': 'success', 'message': 'Setup completed'})

@app.route('/api/game_state')
def game_state():
    return jsonify({
        'current_puzzle': session.get('current_puzzle', 1),
        'score': session.get('score', 0),
        'attempts': session.get('attempts', 0),
        'completed_puzzles': session.get('completed_puzzles', []),
        'game_completed': session.get('game_completed', False),
        'time_elapsed': time.time() - session.get('start_time', time.time())
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 