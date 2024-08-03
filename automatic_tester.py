import subprocess
import os

test_target = 'ece_652_final.py'

def load_expected_results(filename):
    with open(filename, 'r') as file:
        content = file.read().strip()
    
    expected_results = []
    current_result = []
    
    for line in content.split('\n'):
        if line.startswith('Workload'):
            if current_result:
                expected_results.append('\n'.join(current_result).strip())
                current_result = []
        else:
            current_result.append(line)
    
    if current_result:
        expected_results.append('\n'.join(current_result).strip())
    
    return expected_results

def run_test(workload, expected_result):
    result = subprocess.run(['python3', test_target, workload], capture_output=True, text=True)
    output = result.stdout.strip()
    return output == expected_result, output

def main():
    workloads = sorted([f for f in os.listdir() if f.startswith('workload') and f.endswith('.txt')])
    expected_results = load_expected_results('expected_results_652.txt')
    
    report_lines = []
    brief_results = []
    report_lines.append("**********************************************************")
    
    for i, workload in enumerate(workloads):
        if i < len(expected_results):
            expected_result = expected_results[i]
        else:
            expected_result = "No expected result provided"
        
        is_ok, output = run_test(workload, expected_result)
        status = "OK" if is_ok else "NG"
        brief_results.append(f"{i+1}-{status.lower()}")
        
        report_lines.append(f"[{i+1}/{len(workloads)}] Testing {workload} >>>>>>>>>>>>>>>>>  {status}")
        report_lines.append("Your result:")
        report_lines.append(output)
        report_lines.append("Expected result:")
        report_lines.append(expected_result)
        report_lines.append("**********************************************************")
    
    with open('report.txt', 'w') as report_file:
        report_file.write('\n'.join(report_lines))

    print(", ".join(brief_results))

if __name__ == "__main__":
    main()
