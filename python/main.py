def solve_file(file_path):
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        
        N = int(lines[0])
        K = int(lines[1])
        h = [int(line) for line in lines[2:2+N]]  
        
    max_value = -float('inf')
    max_prefix = -float('inf')
    
    for j in range(K, N):
        i = j - K
        current_prefix = h[i] - i
        if current_prefix > max_prefix:
            max_prefix = current_prefix
        
        current_value = max_prefix + h[j] + j
        if current_value > max_value:
            max_value = current_value
    
    return max_value

if __name__ == "__main__":
    for file_path in ["A.txt", "B.txt"]:
            print(f"Максимальное значение для {file_path}: {solve_file(file_path)}")