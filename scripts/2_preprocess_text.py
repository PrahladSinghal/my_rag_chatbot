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

    print(f"[📥] Loaded input file with {len(raw_text)} characters.")
    chunks = chunk_text(raw_text)
    print(f"[🧩] Total chunks created: {len(chunks)}")
    if chunks:
        print(f"[🔍] Sample chunk (first 300 chars):\n{chunks[0][:300]}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(chunk.strip() + "\n\n")

    print(f"[💾] Chunks written to {OUTPUT_FILE}")
    print(f"[✅] {len(chunks)} chunks written to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
