import argparse


if __name__=="__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio_file",type=str,required=True)
    args = vars(ap.parse_args())

    