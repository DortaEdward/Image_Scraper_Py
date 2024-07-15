import requests, os, sys, json, platform, time
from datetime import date, datetime

CWD = os.getcwd()

def downloadImage(url: str, output: str, file_name):
  #fileName = url.replace("https://oss.gtarcade.com/ucms/","").replace("?x-oss-process=image/interlace,1/format,webp,image/resize,m_fill,w_520,h_300","").replace("?x-oss-process=image/interlace,1/format,webp,image/resize,m_fill,w_520,h_300","")
  res = requests.get(url)
  if res.status_code != 200:
      print("ERROR: Could not download", url) 
      return
    
  path_file = os.path.join(output,file_name)
  print("FILENAME:", path_file)
  with open(path_file, "wb") as f:
    f.write(res.content)
    f.close()

def CreateOutputFolder():
  current_date = date.today()
  download_folder = get_download_folder()
  output_path = os.path.join(download_folder,f"{current_date}")
  os.makedirs(output_path,exist_ok=True)
  return output_path 

def Determine_FileType(path: str):
  fileExtension = path.split(".")[1]
  match fileExtension:
     case "json":
        return 0
     case "txt":
        return 1
  return -1

def ParseJson(inputFile: str):
  with open(inputFile,"r") as f:
    data = json.load(f)  
    f.close()
  return data

def ParseTextFile(inputFile: str):
  with open(inputFile, "r") as f:
    data = []
    for line in f:
      line = line.strip()
      if line[-1] == ",": 
        data.append(line[:-1])
      else:
        data.append(line)
    f.close()
  return data

  
def get_download_folder():
  home = os.path.expanduser("~")
  system = platform.system()
  if system == "Windows":
    download_folder = os.path.join(os.environ["USERPROFILE"], "Downloads")
  elif system in ["Linux", "Darwin"]:
    download_folder = os.path.join(home,"Downloads")
  else:
    raise NotImplementedError(f"Unsupported OS: {system}")
  return download_folder

  
def print_help():
  print("Help \n")
  print("Supported Input File Types:")
  print(".json | .txt\n")
  print("Output Directory")
  print("If a output directory is provided, the images will be saved there. Otherwise the images will be saved on the machines download folder\n")
  print("Example: python main.py input.json ./output\n")

def main():
  OUTPUT_FOLDER = None 
  if len(sys.argv) == 1:
     print("Missing Input File and optionally Output destination")
     sys.exit(-1)
  for arg in sys.argv:
    if arg == "-help":
      print_help()
      exit(0)

  args = sys.argv[1:]
  if len(args) >= 2:
    OUTPUT_FOLDER = args[1]
  else:
    OUTPUT_FOLDER = CreateOutputFolder()
  print(OUTPUT_FOLDER)

  inputFile = args[0]

  fileType = Determine_FileType(inputFile)
  if fileType == -1:
     print("ERROR: Input file type not supported. Only input json or txt files")
     os._exit(-1)

  data = ParseJson(inputFile) if fileType == 0 else ParseTextFile(inputFile) 
  for i, src in enumerate(data):
    file_name = f"{i}.png"
    downloadImage(src,OUTPUT_FOLDER,file_name) 


if __name__ == "__main__":
    main()
