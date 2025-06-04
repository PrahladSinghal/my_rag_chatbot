# scripts/2_preprocess_text.py
from langchain.text_splitter import RecursiveCharacterTextSplitter

INPUT_FILE = "../data/raw_combined_text.txt"
OUTPUT_FILE = "../data/processed_chunks.txt"

def chunk_text(text, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    return splitter.split_text(text)

def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        raw_text = f.read()

    chunks = chunk_text(raw_text)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk.strip() + "\n\n")

    print(f"[✅] {len(chunks)} chunks written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
