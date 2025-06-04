from langchain_community.document_loaders import PlaywrightURLLoader

# ✅ Works with JS-heavy websites
loader = PlaywrightURLLoader(
    urls=["https://www.angelone.in/knowledge-center/aadhaar-card/how-to-get-e-aadhaar-password"],
    remove_selectors=["header", "footer", ".sidebar", ".ads", ".nav"],  # optional cleanup
)
docs = loader.load()

print("\n✅ Extracted Content Preview:\n")
print(docs[0].page_content[:1000])


