import subprocess
import re
import os

# 파일 경로 설정
md_file_path = r'C:\Users\Administrator\Desktop\ollama\board.md'

# 파일 내용을 읽어서 변수에 저장
with open(md_file_path, 'r', encoding='utf-8') as file:
    md_content = file.read()

# Ollama에게 전달할 내용이 너무 길면 분할
max_length = 500  # 한 번에 전달할 최대 텍스트 길이 설정
md_parts = [md_content[i:i+max_length] for i in range(0, len(md_content), max_length)]

# Ollama 명령어 텍스트
ollama_base_command = "이 글은 스플랜더라는 게임의 공략이야. 공통되는 내용은 합치고, 다른 내용은 모아서 글로 써줘."

# Ollama에 요청하여 정제된 내용을 저장
refined_content = ""

# 각 분할된 부분을 순차적으로 처리
for part in md_parts:
    ollama_command = f"{ollama_base_command}\n\n{part}"

    print("현재 처리 중인 부분:\n", part)
    
    try:
        # 실시간으로 출력 확인, CREATE_NO_WINDOW 플래그 사용
        with subprocess.Popen(
            ["ollama", "run", "llama3.1", ollama_command],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, encoding='utf-8', shell=True,
            creationflags=subprocess.CREATE_NO_WINDOW  # 콘솔 창 생성 방지
        ) as proc:

            # 출력을 실시간으로 읽어서 화면에 표시
            for line in proc.stdout:
                print(line, end="")  # 실시간으로 출력 결과를 확인

            # 오류가 있는지 확인
            for err_line in proc.stderr:
                print(f"오류 발생: {err_line}")

        proc.wait()

        # stdout에서 모든 결과를 축적
        refined_content += ''.join(proc.stdout)

    except Exception as e:
        print(f"오류가 발생했습니다: {e}")
        break

# .md 파일 생성은 모든 부분을 처리한 후에 진행
output_file_path = r'C:\Users\Administrator\Desktop\ollama\refined_board.md'

# 최종 결과 저장
with open(output_file_path, "w", encoding="utf-8") as file:
    file.write(f"Original File: {md_file_path}\n\n")
    file.write(f"Refined Content:\n{refined_content}\n")

print(f"정제된 내용이 {output_file_path}에 저장되었습니다.")
