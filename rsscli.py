import subprocess
import sys

if len(sys.argv) < 2:
    print("Usage: python3 rsscli.py <rss-url>")
    sys.exit(1)

url = sys.argv[1]
result = subprocess.run(["bash", "rsscore.sh", url],
                        capture_output=True, text=True)

print("\n=== Headlines ===")
print(result.stdout)
