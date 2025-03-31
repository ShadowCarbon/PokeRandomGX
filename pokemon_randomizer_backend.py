from flask import Flask, request, send_file
import os
import subprocess

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RANDOMIZED_FOLDER = 'randomized'
ZX_RANDOMIZER_PATH = 'randomizer/cli.jar'  # Path to Universal Pokémon Randomizer ZX CLI

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RANDOMIZED_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return "Pokémon Randomizer Backend is running!"

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file uploaded", 400
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    options = request.form
    randomized_file_path = randomize_rom(file_path, options)
    
    return send_file(randomized_file_path, as_attachment=True)

def randomize_rom(file_path, options):
    randomized_file_path = os.path.join(RANDOMIZED_FOLDER, f"randomized_{os.path.basename(file_path)}")
    
    # Prepare CLI options based on user-selected options
    cli_options = ['java', '-jar', ZX_RANDOMIZER_PATH, '--input', file_path, '--output', randomized_file_path]
    
    # Add selected options to CLI command
    add_randomization_options(cli_options, options)
    
    # Run Universal Pokémon Randomizer ZX CLI with the selected options
    try:
        subprocess.run(cli_options, check=True)
    except subprocess.CalledProcessError as e:
        return f"Error randomizing ROM: {e}", 500
    
    return randomized_file_path

def add_randomization_options(cli_options, options):
    # Trainer randomization
    if 'randomizeTrainers' in options:
        cli_options.append('--randomize-trainers')
    if 'randomizeWild' in options:
        cli_options.append('--randomize-wild')
    if 'randomizeStarters' in options:
        cli_options.append('--randomize-starters')
    if 'randomizeAbilities' in options:
        cli_options.append('--randomize-abilities')
    if 'randomizeEvolutions' in options:
        cli_options.append('--randomize-evolutions')
    if 'randomizeMoves' in options:
        cli_options.append('--randomize-moves')
    if 'randomizeStatic' in options:
        cli_options.append('--randomize-static')

    # Shop randomization
    if 'randomizePokemartItems' in options:
        cli_options.append('--randomize-pokemart-items')
    if 'randomizeHeldItems' in options:
        cli_options.append('--randomize-held-items')
    if 'randomizeTMs' in options:
        cli_options.append('--randomize-tms')
    if 'randomizeKeyItems' in options:
        cli_options.append('--randomize-key-items')
    if 'randomizeItemPrices' in options:
        cli_options.append('--randomize-item-prices')

    # Hidden items and TM randomization
    if 'randomizeHiddenItems' in options:
        cli_options.append('--randomize-hidden-items')
    if 'randomizeHiddenItemLocations' in options:
        cli_options.append('--randomize-hidden-item-locations')
    if 'randomizeTMLocations' in options:
        cli_options.append('--randomize-tm-locations')
    if 'randomizeTMCompatibility' in options:
        cli_options.append('--randomize-tm-compatibility')

    # Additional randomization features
    if 'randomizeTypes' in options:
        cli_options.append('--randomize-types')
    if 'randomizeMovesetsByGeneration' in options:
        cli_options.append('--randomize-movesets-by-generation')
    if 'randomizeStats' in options:
        cli_options.append('--randomize-stats')
    if 'randomizeShiny' in options:
        cli_options.append('--randomize-shiny')
    if 'randomizeMovesetByType' in options:
        cli_options.append('--randomize-moveset-by-type')
    if 'randomizeGender' in options:
        cli_options.append('--randomize-gender')
    if 'randomizeLegendary' in options:
        cli_options.append('--randomize-legendary')
    if 'randomizeAbilitiesByGeneration' in options:
        cli_options.append('--randomize-abilities-by-generation')
    if 'randomizeShinyOdds' in options:
        cli_options.append('--randomize-shiny-odds')
    if 'randomizeSizes' in options:
        cli_options.append('--randomize-sizes')
    if 'randomizeColors' in options:
        cli_options.append('--randomize-colors')
    if 'randomizeEvolutionMethods' in options:
        cli_options.append('--randomize-evolution-methods')
    if 'randomizeAbilitiesBySpecies' in options:
        cli_options.append('--randomize-abilities-by-species')
    if 'randomizeTradeItems' in options:
        cli_options.append('--randomize-trade-items')
    if 'randomizeMovesetByLevel' in options:
        cli_options.append('--randomize-moveset-by-level')
    if 'randomizeTrainerTeams' in options:
        cli_options.append('--randomize-trainer-teams')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
