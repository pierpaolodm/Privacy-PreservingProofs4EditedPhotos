#!/usr/bin/env python3

import argparse
import subprocess
from scripts.util import generate_circuit, generate_circuit_input, resize_image, tile_image


def tile_proof(tile_idx,pot_path):
    """
    Generate the proof for the tile circuit
    :param tile_idx: index of the tile to generate the proof for
    :param pot_path: path to the pot file
    """
    circuit_name = f'tile_{tile_idx}'
    input_path = f'./input/tile_{tile_idx}.json'

    print('\n====================================')
    print(f'Generating proof for tile {tile_idx}')

    for name,command in {'COMPILE':f'./scripts/compile_circuit.sh ./circuits/tiles/{circuit_name}.circom {input_path} ',
                         'SETUP':f'./scripts/proving_system/setup_prover.sh {circuit_name} {pot_path}',
                         'PROVE':f'./scripts/proving_system/prover.sh {circuit_name} '}.items():
        
        res = subprocess.run(command, shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if res.returncode != 0:
            raise Exception(f'Error in command: {command}\n{res.stderr}')
        else:
            print(f'Command {name} executed successfully')
    


def generate_proof(image_path,tiles_num,rh,rw,POT_PATH):
    """
    Generate the proof for the resize and hash circuit
    :param image_path: path to the image to resize and hash
    :param tiles_num: number of tiles to split the image into
    :param rh: resize height
    :param rw: resize width
    :param POT_PATH: path to the pot file
    """
    image_name = image_path.split('/')[-1].split('.')[0]
    print(f'GENERATING PROOF FOR IMAGE {image_name} WITH {tiles_num} TILES')

    CIRCUIT_TEMPLATE = './circuits/base/resize_and_hash.circom'
    tiles = tile_image(image_path,tiles_num)

    for i,tile in enumerate(tiles):
        resize_tile = resize_image(tile,rh,rw)
        generate_circuit_input(tile,resize_tile,f'tile_{i}.json')

        input_parameters = {'HFULL':tile.shape[0],
                            'WFULL':tile.shape[1],

                            'HRESIZE':resize_tile.shape[0],
                            'WRESIZE':resize_tile.shape[1]}
        generate_circuit(input_parameters,CIRCUIT_TEMPLATE,f'tile_{i}')
        tile_proof(i,POT_PATH)




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate proof for an image circuit.')

    parser.add_argument('--image', type=str, required=True, help='Path to the image.')
    parser.add_argument('--N', type=int, required=True, help='Number of tiles to split the image into.')
    parser.add_argument('--height', type=int, required=True, help='Resize height.')
    parser.add_argument('--width', type=int, required=True, help='Resize width.')
    parser.add_argument('--pot', type=str, required=True, help='Path to the pot file.')

    args = parser.parse_args()

    generate_proof(args.image, args.N, args.height, args.width, args.pot)
