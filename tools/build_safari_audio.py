"""Build Safari/iPad AAC alternatives from the credited, shipped Ogg effects.
Run after either audio builder. A limiter leaves headroom for AAC reconstruction peaks.
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parent.parent

def convert(source):
    target=source.with_suffix('.m4a')
    if target.exists() and target.stat().st_mtime>=max(source.stat().st_mtime,Path(__file__).stat().st_mtime):return
    subprocess.run(['ffmpeg','-v','error','-nostdin','-y','-i',str(source),'-map_metadata','-1','-af','alimiter=limit=0.75:level=false,volume=-2dB','-ac','1','-ar','44100','-c:a','aac','-b:a','96k','-movflags','+faststart',str(target)],check=True)

def main():
    sources=[*sorted((ROOT/'assets/audio/sfx').glob('*.ogg')),*sorted((ROOT/'assets/audio/skills').glob('*.ogg'))]
    with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(convert,sources))
    print('Safari AAC alternatives ready:',len(sources))
if __name__=='__main__':main()
