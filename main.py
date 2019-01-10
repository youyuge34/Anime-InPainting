import os
import cv2
import random
import numpy as np
import torch
import argparse
from shutil import copyfile
from src.config import Config
from src.edge_connect import EdgeConnect


def main(mode=None, config=None):
    r"""starts the model

    Args:
        mode (int): 1: train, 2: test, 3: eval, reads from config file if not specified
                    4: demo_patch,
    """

    if mode == 4:
        config = load_config_demo(mode, config=config)
    else:
        config = load_config(mode)

    # init environment
    if (config.DEVICE == 1 or config.DEVICE is None) and torch.cuda.is_available():
        os.environ['CUDA_VISIBLE_DEVICES'] = ','.join(str(e) for e in config.GPU)
        config.DEVICE = torch.device("cuda")
        torch.backends.cudnn.benchmark = True  # cudnn auto-tuner
    else:
        config.DEVICE = torch.device("cpu")
    # print(torch.cuda.is_available())
    print('DEVICE is:', config.DEVICE)

    # set cv2 running threads to 1 (prevents deadlocks with pytorch dataloader)
    cv2.setNumThreads(0)

    # initialize random seed
    torch.manual_seed(config.SEED)
    torch.cuda.manual_seed_all(config.SEED)
    np.random.seed(config.SEED)
    random.seed(config.SEED)

    # enable the cudnn auto-tuner for hardware.
    torch.backends.cudnn.benchmark = True

    # build the model and initialize
    model = EdgeConnect(config)
    model.load()

    # model training
    if config.MODE == 1:
        config.print()
        print('\nstart training...\n')
        model.train()

    # model test
    elif config.MODE == 2:
        print('\nstart testing...\n')
        # import time
        # start = time.time()
        with torch.no_grad():
            model.test()
        # print(time.time() - start)

    # eval mode
    elif config.MODE == 3:
        print('\nstart eval...\n')
        with torch.no_grad():
            model.eval()

    elif config.MODE == 4:
        if config.DEBUG:
            config.print()
        print('model prepared.')
        return model


def load_config(mode=None):
    r"""loads model config 

    Args:
        mode (int): 1: train, 2: test, 3: eval, reads from config file if not specified
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '--checkpoints', type=str, default='./checkpoints',
                        help='model checkpoints path (default: ./checkpoints)')
    parser.add_argument('--model', type=int, choices=[1, 2, 3, 4],
                        help='1: edge model, 2: inpaint model, 3: edge-inpaint model, 4: joint model')

    # test mode
    if mode == 2:
        parser.add_argument('--input', type=str, help='path to the input images directory or an input image')
        parser.add_argument('--mask', type=str, help='path to the masks directory or a mask file')
        parser.add_argument('--edge', type=str, help='path to the edges directory or an edge file')
        parser.add_argument('--output', type=str, help='path to the output directory')

    args = parser.parse_args()
    config_path = os.path.join(args.path, 'config.yml')

    # create checkpoints path if does't exist
    if not os.path.exists(args.path):
        os.makedirs(args.path)

    # copy config template if does't exist
    if not os.path.exists(config_path):
        copyfile('./config.yml.example', config_path)

    # load config file
    config = Config(config_path)

    # train mode
    if mode == 1:
        config.MODE = 1
        if args.model:
            config.MODEL = args.model 

        if config.SKIP_PHASE2 is None:
            config.SKIP_PHASE2 = 0
        if config.MODEL == 2 and config.SKIP_PHASE2 == 1:
            raise Exception("MODEL is 2, cannot skip phase2! trun config.SKIP_PHASE2 off or just use MODEL 3.")

    # test mode
    elif mode == 2:
        config.MODE = 2
        config.MODEL = args.model if args.model is not None else 3
        config.INPUT_SIZE = 0

        if args.input is not None:
            config.TEST_FLIST = args.input

        if args.mask is not None:
            config.TEST_MASK_FLIST = args.mask

        if args.edge is not None:
            config.TEST_EDGE_FLIST = args.edge

        if args.output is not None:
            config.RESULTS = args.output

    # eval mode
    elif mode == 3:
        config.MODE = 3
        config.MODEL = args.model if args.model is not None else 3

    return config


def load_config_demo(mode, config):
    r"""loads model config

    Args:
        mode (int): 4: demo_patch
    """
    print('load_config_demo----->')
    if mode == 4:
        config.MODE = 4
        config.MODEL = 3
        config.INPUT_SIZE = 0

    return config


if __name__ == "__main__":
    main()
