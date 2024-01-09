import argparse
import subprocess

def main():
    parser = argparse.ArgumentParser(description='PTT2000 PROJECT V0.')

    # Ajoutez vos options ici
    parser.add_argument('-a', action='store_true', help='Option A')
    # parser.add_argument('-b', type=str, help='Option B')

    args = parser.parse_args()

    if args.a:
        subprocess.run(["python3", "test2.py"])

    #if args.b:
     #   print(f'Option B activée avec la valeur : {args.b}')

if __name__ == "__main__":
    main()
