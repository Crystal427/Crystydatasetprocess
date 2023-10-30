import os
import argparse
from transformers import AutoModelForCausalLM, AutoTokenizer

DEFAULT_CKPT_PATH = 'Qwen/Qwen-7B-Chat'

def load_model_tokenizer(checkpoint_path, cpu_only):
    tokenizer = AutoTokenizer.from_pretrained(checkpoint_path)

    device = "cpu" if cpu_only else "cuda"
    model = AutoModelForCausalLM.from_pretrained(checkpoint_path).to(device).eval()

    return model, tokenizer

def extract_title_from_file_content(content, model, tokenizer, device):
    prompt = f"我需要你从这段里面找到文章的标题，下面是内容:\n{content}\n你只需要回复你认为的文章标题,不要自己创造新的标题。"
    input_ids = tokenizer.encode(prompt, return_tensors="pt").to(device)
    out = model.generate(input_ids)
    title = tokenizer.decode(out[0], skip_special_tokens=True)
    return title

def main():
    parser = argparse.ArgumentParser(description='Extract titles from files in a directory using QWen model.')
    parser.add_argument("-c", "--checkpoint-path", type=str, default=DEFAULT_CKPT_PATH,
                        help="Checkpoint name or path, default to %(default)r")
    parser.add_argument("--cpu-only", action="store_true", help="Run with CPU only")
    parser.add_argument("-d", "--directory", type=str, required=True, help="Directory to read files from")
    parser.add_argument("-x", "--num-chars", type=int, default=500, help="Number of characters to read from each file")
    args = parser.parse_args()

    model, tokenizer = load_model_tokenizer(args.checkpoint_path, args.cpu_only)
    device = "cpu" if args.cpu_only else "cuda"

    for root, _, files in os.walk(args.directory):
        for filename in files:
            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read(args.num_chars).replace("\n", " ")  # Replacing newlines with spaces
            
            title = extract_title_from_file_content(content, model, tokenizer, device)
            print(f"Original filename: {filename}, Extracted title: {title}")

if __name__ == "__main__":
    main()
