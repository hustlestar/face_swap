import logging
import os
import subprocess
import click

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', )
logger = logging.getLogger(__name__)


def prepare_swap_command(input_reel_path, output_reel_path, face_img_path):
    return ["G:\\OLD_DISK_D_LOL\\Projects\\FACE_SWAP\\roop_env\\Scripts\\python.exe", "G:\\OLD_DISK_D_LOL\\Projects\\FACE_SWAP\\roop\\run.py",
            '--target',
            input_reel_path,
            '--source',
            face_img_path,
            '-o',
            output_reel_path,
            '--execution-provider',
            'cuda',
            '--keep-fps',
            '--output-video-quality',
            '1',
            '--frame-processor',
            'face_swapper'
            ]


def run_face_swap(input_root_dir, output_dir, face_img_path):
    models_dirs = os.listdir(input_root_dir)
    counter = 1
    for model_dir in models_dirs:
        logger.info(">" * 100)
        logger.info(f"Processing model {model_dir}...")
        model_dir_path = os.path.join(input_root_dir, model_dir)
        if os.path.isdir(model_dir_path):
            for initial_reel in os.listdir(model_dir_path):
                logger.info(f"Processing {counter} file {initial_reel}...")
                # if initial_reel.endswith(".mp4"):
                #     logger.info(f"Skipping {initial_reel}...")
                #     continue
                input_reel_path = os.path.join(model_dir_path, initial_reel)
                output_reel_path = os.path.join(output_dir, model_dir, initial_reel)
                if os.path.exists(output_reel_path):
                    logger.info(f"Reel {initial_reel} already processed. Skipping")
                    continue
                os.makedirs(os.path.dirname(output_reel_path), exist_ok=True)
                command = prepare_swap_command(input_reel_path=input_reel_path, output_reel_path=output_reel_path, face_img_path=face_img_path)
                # run_command(['pip', 'freeze'])
                run_command(command)
                logger.info(f"Finished processing reel {initial_reel}")
                counter += 1
        logger.info("<" * 100)
        logger.info(f"Finished processing all reels for model {model_dir}")


def run_command(command):
    str_command = ' '.join(command).replace('\\\\', '\\')
    logger.info(f"Running command: {str_command}")
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    out, err = proc.communicate()
    logger.info(out.decode())
    logger.info(err.decode())


@click.command()
@click.option('-i', '--input', type=click.Path(exists=True), help='Input directory')
@click.option('-o', '--output', type=click.Path(), help='Output directory')
@click.option('-f', '--face', type=click.Path(), help='Face image')
def main(input_dir, output_dir, face_img_path):
    run_face_swap(input_dir, output_dir, face_img_path)


if __name__ == "__main__":
    run_face_swap("E:\\PUSSY_FIRE\\INITIAL\\black",
                  "E:\\PUSSY_FIRE\\PROCESSED\\victoria",
                  'G:\\OLD_DISK_D_LOL\\Projects\\FACE_SWAP\\roop\\data\\input\\victoria.png')
    run_face_swap("E:\\PUSSY_FIRE\\INITIAL\\blonde",
                  "E:\\PUSSY_FIRE\\PROCESSED\\julliana",
                  'G:\\OLD_DISK_D_LOL\\Projects\\FACE_SWAP\\roop\\data\\input\\julliana.png')
    run_face_swap("E:\\PUSSY_FIRE\\INITIAL\\tan_black",
                  "E:\\PUSSY_FIRE\\PROCESSED\\nikki",
                  'G:\\OLD_DISK_D_LOL\\Projects\\FACE_SWAP\\roop\\data\\input\\new_nikki.png')
