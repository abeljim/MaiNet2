import os 
import sys 
import argparse 
from util.prepro import squad_prepro

parser = argparse.ArgumentParser(description="Model Parameters")

# Mode 
parser.add_argument(
    '--mode',
    default='none',
    type=str,
    help='mode of program prepro/train/demo')


def main(args):

    if(args.mode == "prepro"):
        print("Preprocessing Starting ...")
        squad_prepro(args)

    elif(args.mode == "train"):
        print("Training Starting ...") 

    elif(args.mode == "demo"):
        print("Demo Mode")

    else:
        print("No Mode Selected")
        print("Program Stop")

if __name__ == '__main__':
    main(parser.parse_args())
