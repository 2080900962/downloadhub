import requests
import time
from concurrent.futures import ThreadPoolExecutor
import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

test_urls = [
    "https://nodejs.org/dist/v20.0.0/node-v20.0.0-win-x64.zip",
    "https://github.com/git/git/archive/refs/tags/v2.40.0.zip",
    "https://dl.google.com/chrome/install/latest/chrome_installer.exe",
    "https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-2023.03-Windows-x86_64.exe",
    "https://download.pytorch.org/whl/torch-2.0.0-cp310-cp310-win_amd64.whl",
    "https://invalid-url-test-404.com/file.zip",
    "https://httpstat.us/500",
    "https://httpstat.us/timeout?sleep=10000"
]

def test_single_url(url):
    print(f"\n测试: {url}")
    start = time.time()

    try:
        resp = requests.post(
            'http://localhost:5000/api/search',
            json={'url': url},
            timeout=30
        )
        elapsed = time.time() - start

        if resp.status_code == 200:
            data = resp.json()
            print(f"✓ 成功 ({elapsed:.2f}s)")
            print(f"  找到 {len(data['results'])} 个源")
            print(f"  最快源: {data['fastest']['speed'] if data['fastest'] else 'N/A'}")
            return {'success': True, 'time': elapsed, 'sources': len(data['results'])}
        else:
            print(f"✗ 失败: {resp.status_code}")
            return {'success': False, 'time': elapsed, 'error': resp.status_code}
    except Exception as e:
        elapsed = time.time() - start
        print(f"✗ 异常: {str(e)}")
        return {'success': False, 'time': elapsed, 'error': str(e)}

print("=" * 60)
print("开始压力测试")
print("=" * 60)

results = []
for url in test_urls:
    result = test_single_url(url)
    result['url'] = url
    results.append(result)
    time.sleep(1)

print("\n" + "=" * 60)
print("测试报告")
print("=" * 60)

success_count = sum(1 for r in results if r['success'])
total_count = len(results)
avg_time = sum(r['time'] for r in results) / total_count

print(f"\n成功率: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
print(f"平均响应时间: {avg_time:.2f}s")

print("\n失败案例:")
for r in results:
    if not r['success']:
        print(f"  - {r['url']}")
        print(f"    错误: {r.get('error', 'unknown')}")

with open('test_report.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\n详细报告已保存到 test_report.json")
