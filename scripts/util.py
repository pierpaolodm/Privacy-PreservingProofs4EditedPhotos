#!/usr/bin/env python3


import os
import json
import cv2
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
import numpy as np



def generate_circuit(info, circuit_template, id = None):
    """
    Generate a circuit from a template
    :param info: dictionary with the information to replace in the template
    :param circuit_template: path to the template
    :param id: id of the circuit

    """
    out_circuit = circuit_template.split('/')[-1].split('.')[0]
    os.makedirs('circuits/tiles',exist_ok=True)

    with open(circuit_template, 'r') as infile:
        circuit = infile.read()
        for k,v in info.items():
            circuit = circuit.replace(k, str(v))
        circuit = circuit.replace('//MAIN', '')
        
        id = f'{id}' if id is not None else f'{out_circuit}'
        out_path = f'circuits/tiles/{id}.circom'
        with open(out_path, 'w') as outfile:
            outfile.write(circuit)
    return out_path

def resize_image(image_path, height, width):
    """
    Resize an image to the given dimensions.
    :param image_path: Path to the image to resize or array.
    :param height: Height of the resized image.
    :param width: Width of the resized image.
    :return: the resized image.
    """
    image = cv2.imread(image_path,cv2.IMREAD_COLOR) if isinstance(image_path,str) else image_path
    original_height, original_width, _ = image.shape

    if (original_height-1) % (height-1) != 0 or (original_width-1) % (width-1) != 0:
        divisors_h = [v+1 for v in range(1, (original_height - 1)//2) if (original_height - 1) % v == 0]
        divisors_w = [v+1 for v in range(1, (original_width - 1)//2) if (original_width - 1) % v == 0]
        raise ValueError(f" The image cannot be resized to the given dimensions.\n \
                            The height must be one of this numbers: {divisors_h}\n \
                            The width must be one of this numbers: {divisors_w}")

    return (
        (
            tf.compat.v1.image.resize(
                image,
                [height, width],
                align_corners=True,
                method=tf.image.ResizeMethod.BILINEAR,
            )
        )
        .numpy()
        .round()
        .astype(np.uint8)
    )

def tile_image(image_path, num_tiles):
    """
    Tile an image into a specified number of tiles along a specified dimension
    :param image_path: path to image or array
    :param num_tiles: number of tiles to generate along the specified dimension
    :return: list of tiles
    """
    
    image = cv2.imread(image_path,cv2.IMREAD_COLOR) if isinstance(image_path,str) else image_path
    img_height, img_width, _ = image.shape
    tile_size = (img_height if (img_height > img_width) else img_width) // num_tiles

    tiles = list()
    for i in range(num_tiles):
        start = i * tile_size
        end = ((i + 1) * tile_size) if (i != (num_tiles - 1)) else None

        tile = image[start:end, :] if (img_height > img_width) else image[:, start:end, :]
        tiles.append(tile)

    return tiles
    

def generate_circuit_input(full_img,rsz_img, file_name = 'input.json'):
    """
    Generate the input for the circuit
    :param full_img: path to the full image or array
    :param rsz_img: path to the resized image or array
    :return: dictionary with the input for the circuit
    """
    full_img = cv2.imread(full_img,cv2.IMREAD_COLOR).astype(np.uint8) \
               if isinstance(full_img,str) else full_img.astype(np.uint8)
    
    rsz_img = cv2.imread(rsz_img,cv2.IMREAD_COLOR).astype(np.uint8) \
              if isinstance(rsz_img,str) else rsz_img.astype(np.uint8)

    json_input = {'full_image':full_img.astype(str).tolist(),
                  'resize_image':rsz_img.astype(str).tolist()}

    os.makedirs('input',exist_ok=True)
    with open(f'./input/{file_name}', 'w') as out_file:
        json.dump(json_input, out_file)
    

if __name__ == '__main__':
    raise ValueError('This script is not meant to be executed directly')
